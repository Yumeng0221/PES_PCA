# This script extracts all stationary points from Gaussian relaxed scan calculations.
# Usage:
#   Run the script and provide the directory containing the Gaussian output files.
# Notes:
#   - Update the "level of theory" in the script to match the one used in your calculations (line 25). 
#   - If your scan includes more than 30 steps, adjust the number of columns accordingly (line 28). 

import os
import re
import pandas as pd
import numpy as np

def main():
    print('The output orientations will be stored into CSV files; filenames are formatted as input file & energy.')
    print('Use current directory if input/output directory is empty.')
    
    # load input file directory
    input_dir = input("Enter the directory path containing the .log files: ").strip()
    if not input_dir:
        input_dir = os.getcwd()
    if not input_dir.endswith(os.path.sep):
        input_dir += os.path.sep
    print(f" Input Directory: {input_dir}")

    functional_string = "RB3LYP" # adjust based on your level of theory
    
    # Create the output file DataFrame (supports up to 30 energies -> 31 columns including the first label), add more as needed
    columns = ["Filename/PC"] + [f"E{i}" for i in range(1, 31)]
    final_df = pd.DataFrame(columns=columns)

    found_log = False  # ← initialize to avoid NameError

    for filename in os.listdir(input_dir):
        if filename.endswith(".log"):
            found_log = True

            file_path = os.path.join(input_dir, filename)
            filename_base = os.path.splitext(filename)[0]

            with open(file_path, 'r') as file:
                print(f" Now processing file: {file_path}")
                lines = file.readlines()

            energy_positions = []
            energy_values = []
            pc1_list = []
            pc2_list = []

            # Extract energy positions
            for i, line in enumerate(lines):
                pattern = rf"E\({functional_string}\)\s*=\s*(-?\d+\.\d+)"
                match = re.search(pattern, line)
                if match:
                    energy_value = float(match.group(1))
                    energy_positions.append((i, energy_value))

            # Find energies before "Stationary point found"
            energies_before_stationary = []
            for idx in range(len(energy_positions) - 1):
                current_line, energy_value = energy_positions[idx]
                next_line, _ = energy_positions[idx + 1]
                if any("Stationary point found" in lines[j] for j in range(current_line, next_line)):
                    energies_before_stationary.append((current_line, energy_value))
                    energy_values.append(energy_value)

            # Handle the last energy (if followed by a stationary point later)
            if energy_positions:
                last_line, last_energy = energy_positions[-1]
                if any("Stationary point found" in lines[j] for j in range(last_line, len(lines))):
                    energies_before_stationary.append((last_line, last_energy))
                    energy_values.append(last_energy)

            # For each energy line, find the next stationary point and back-search for PC1/PC2
            for e_idx, _e_val in energies_before_stationary:
                stationary_idx = None
                for j in range(e_idx + 1, len(lines)):
                    if "Stationary point found" in lines[j]:
                        stationary_idx = j
                        break
            
                if stationary_idx is not None:
                    # Backward search for PC1
                    for k in range(stationary_idx, e_idx - 1, -1):
                        if "PC1" in lines[k]:
                            items = lines[k].split()  
                            pc1_list.append(items[-1].strip())
                            break

                    # Backward search for PC2
                    for k in range(stationary_idx, e_idx - 1, -1):
                        if "PC2" in lines[k]:
                            items = lines[k].split()  
                            pc2_list.append(items[-1].strip())
                            break        

            first_row = [f"{filename_base}_pc"] + energy_values[:30]
            second_row = ['pc1'] + pc1_list
            third_row = ['pc2'] + pc2_list

            # Pad to ensure 17 columns
            while len(first_row) < 30:
                first_row.append(np.nan)
            while len(second_row) < 30:
                second_row.append(np.nan)
            while len(third_row) < 30:
                third_row.append(np.nan)

            final_df.loc[len(final_df)] = first_row
            final_df.loc[len(final_df)] = second_row
            final_df.loc[len(final_df)] = third_row

            print(' Num of stationary points found is ' + str(len(energies_before_stationary)))
    
    if found_log:
        out_path = os.path.join(input_dir, "final_output.csv")
        final_df.to_csv(out_path, index=False)
            
        pc1_vals = []
        pc2_vals = []
        energy_vals = []
            
        # Process every 3-row block in final_df: rows [energy, pc1, pc2]
        # Your triplets start at row 0, so start from i=0 with step 3
        for i in range(0, len(final_df), 3):
            if i + 2 >= len(final_df):
                break  # ensure complete triplet
            
            energy_line = final_df.iloc[i].tolist()[1:]       # skip first label cell
            pc1_line   = final_df.iloc[i + 1].tolist()[1:]
            pc2_line   = final_df.iloc[i + 2].tolist()[1:]

            for e, x, y in zip(energy_line, pc1_line, pc2_line):
                # Skip if any is NaN/empty
                if pd.notna(e) and pd.notna(x) and pd.notna(y) and (str(e) != '') and (str(x) != '') and (str(y) != ''):
                    try:
                        energy_vals.append(float(e))
                        pc1_vals.append(float(x))
                        pc2_vals.append(float(y))
                    except ValueError:
                        # If parsing fails for any cell, skip that triplet
                        continue
                    
        df = pd.DataFrame({
            "pc1": pc1_vals,
            "pc2": pc2_vals,
            "energy": energy_vals
        })
            
        # Round pc1 and pc2 to 2 decimal places
        df["pc1_rounded"] = df["pc1"].round(2)
        df["pc2_rounded"] = df["pc2"].round(2)

        # === Step 3: Pivot to matrix format ===
        df_matrix = df.pivot_table(
            index="pc2_rounded",
            columns="pc1_rounded",
            values="energy",
            aggfunc="mean"  # handles duplicates after rounding
        )

        # Sort rows and columns
        df_matrix = df_matrix.sort_index().sort_index(axis=1)

        # === Step 4: Export to Excel ===
        excel_path = os.path.join(input_dir, "energies.xlsx")
        df_matrix.to_excel(excel_path)
        print(f"\nAll done! energies.xlsx saved to:\n{excel_path}\n(Also wrote {out_path})")
    else:
        print("No .log files found in the specified directory.")

if __name__ == "__main__":
    main()
