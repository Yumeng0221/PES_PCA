# Construct a 3D Potential Energy Surface (PES) plot.

from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main(): 
    
    data = pd.read_excel('energies.xlsx', header=None) # Update the energy filename here if needed. 

    x = data.iloc[0, 1:].values
    y = data.iloc[1:, 0].values
    z = data.iloc[1:, 1:].values

    # Convert x and y to numeric if needed
    x = pd.to_numeric(x, errors='coerce')
    y = pd.to_numeric(y, errors='coerce')

    # Make meshgrid
    X, Y = np.meshgrid(x, y)

    # Create a 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(X, Y, z, cmap='coolwarm', edgecolor='k', linewidth=0.5)

    # Add color bar and labels
    fig.colorbar(surf, ax=ax, shrink=0.35, aspect=10)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_zlabel('Energy (unit in Hartree)')
    ax.set_title('3D Surface Plot of Potential Energy Surface')

    plt.show()

if __name__=="__main__":
    main()
