# Construct PES based on the energies.xlsx

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Load the data
    data = pd.read_excel('energies_diff.xlsx', header=None)

    x = data.iloc[0, 1:].values
    y = data.iloc[1:, 0].values
    z = data.iloc[1:, 1:].values

    # Convert x and y to numeric if needed
    x = pd.to_numeric(x, errors='coerce')
    y = pd.to_numeric(y, errors='coerce')

    # Make meshgrid
    X, Y = np.meshgrid(x, y)

    # Plot the contour
    plt.figure(figsize=(10, 8))
    cp = plt.contourf(X, Y, z, levels=20, cmap='coolwarm')
    plt.colorbar(cp)

    # Label axes
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 1')
    plt.title('2D Contour Plot of Energies (unit in hartree)')

    plt.show()

if __name__=="__main__": 
    main()
