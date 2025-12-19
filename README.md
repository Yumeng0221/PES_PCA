**Overview**

Constructing low-dimensional PES representations for reactions involving many coupled internal coordinates. 

**This workflow:**
1. Uses PCA to identify dominant structural variations from multiple internal coordinates (e.g., bond lengths, angles, dihedrals),
2. Uses the resulting principal components (PC1 and PC2) as physically meaningful scan axes,
3. Performs relaxed surface scans using electronic structure software (e.g., Gaussian),
4. Visualizes 2D or 3D PESs.

**Requirements**

Python ≥ 3.8

Required Python packages:
numpy
pandas
scikit-learn
matplotlib

Quantum chemistry software for scan calculations:
Gaussian 16 (examples provided),
but the workflow can be adapted to other packages.

**Example Usage**
A Jupyter Notebook example is provided in the examples/ directory to walk you through the complete procedure step by step.
