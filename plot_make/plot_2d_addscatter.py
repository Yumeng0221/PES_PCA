# Generate a potential energy surface (PES) plot using data from 'energies.xlsx' 
# (produced by scan_energies_collect.py). Scatter points represent critical points 
# such as reactants, transition states, and products. 
# Requires the initial data files (data.xlsx) for the scatter plot to be located in the same directory.

from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Calculate scatter points axis
file_path = input("Enter the Excel file containing the variables (e.g., data.xlsx): ").strip()
data = pd.read_excel(file_path)
labels = data['Unnamed: 0']
numeric_data = data.drop(columns = ['Unnamed: 0'])
labels = data.iloc[:, 0]
mean_values = np.around(numeric_data.mean(), decimals=4) #calculate the mean 
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(numeric_data)  # shape: (n_samples, 2)

# Load the PES data
data = pd.read_excel('energies.xlsx', header=None) #modify here is other energy table is using. 
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

for i, (label, (pc1, pc2)) in enumerate(zip(labels, pca_coords)):
    plt.scatter(pc1, pc2, facecolor="yellow", edgecolor="black")
    plt.text(pc1 + 0.03, pc2 + 0.03, label, fontsize=15, color="black")
    
# Label axes
plt.xlabel('Principal Component 1',fontsize=15)
plt.ylabel('Principal Component 2',fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Potential Energy Surface',fontsize=15)
plt.savefig("PES_plot_with_scatter.png", dpi=600, bbox_inches="tight") 
plt.show()