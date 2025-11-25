# Generate information using PCA for construct potential energy sruface
# Yumeng Cao Dec. 11th, 2024
# modified on Jul 7th for input directory name

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import os

def main():
    # input working directory and filename
    input_dir = input("Enter the directory path containing the Excel file: ").strip()
    file_name = input("Enter the Excel file name (e.g., data.xlsx): ").strip()

    file_path = os.path.join(input_dir, file_name)
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    data = pd.read_excel(file_path)
    labels = data['Unnamed: 0']
    numeric_data = data.drop(columns = ['Unnamed: 0'])

    mean_values = np.around(numeric_data.mean(), decimals=4) #calculate the mean 

    # Apply PCA analysis
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(numeric_data)

    # Create a new DataFrame with the PCA results
    pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
    pca_df['label'] = labels
    coefficients = np.around(pca.components_, decimals=4) # Generate PCA coefficient

    #Save the plot
    plt.figure()
    for label in pca_df['label'].unique():
        subset = pca_df[pca_df['label'] == label]
        plt.scatter(subset['PC1'], subset['PC2'], label=label)

    plt.title('PCA of Structures')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend()
    plt.grid(True)
    plot_path = os.path.join(input_dir, "PCA_plot.png")
    plt.savefig(plot_path, dpi=300) 

    # Generate addition Gaussian input line
    output_PC1 = "PC1()=" + "+".join(
        [f"({coeff})*(R{col}-{mean})" for coeff, col, mean in zip(coefficients[0], numeric_data.columns, mean_values)]
    )

    output_PC2 = "PC2()=" + "+".join(
        [f"({coeff})*(R{col}-{mean})" for coeff, col, mean in zip(coefficients[1], numeric_data.columns, mean_values)]
    )

    # Save results to pca_results.txt
    output_file_path = os.path.join(input_dir, "pca_results.txt")
    with open(output_file_path, 'w') as file: 
        file.write("Coefficient: \n")
        for row in coefficients:
            file.write(str(row) + "\n")
        file.write("\nMean_values: \n")
        file.write(str(mean_values) + "\n")

        file.write("\nGIC additional line: \n")
        file.write(str(output_PC1) + "\n")
        file.write(str(output_PC2) + "\n")

    print(f"Results saved to {output_file_path}")

if __name__=="__main__":
    main()