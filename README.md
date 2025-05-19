# Master Thesis: Quantum Approaches to Solving Sudoku Puzzles

This repository contains the code developed for my master thesis, "Quantum Approaches to Solving Sudoku Puzzles". 
The thesis investigates the application of quantum computing techniques, using Qiskit, and by Clifford algebra packages in MATLAB to solve Sudoku puzzles.

## Repository Contents

* **`MATLAB/`**: Contains MATLAB scripts implementing algorithms for solving Sudoku puzzles by Clifford algebra signature.
* **`Qiskit/`**: Contains Python scripts and Jupyter notebooks that explore quantum algorithms, such as Grover's algorithm, and quantum counting for solving Sudoku puzzles using the Qiskit framework.
* **`README.md`**: This file, providing an overview of the repository.

## Prerequisites

To run the code in this repository, you will need the following:

* **MATLAB**: Version R2020b or later (recommended)
* **Python**: Version 3.8 or later
* **Qiskit**: Install using pip:
    ```bash
    pip install qiskit
    ```
* **NumPy**: Install using pip:
    ```bash
    pip install numpy
    ```
## Installation

### MATLAB `clifford_signature` Toolbox

1.  Download the `clifford_signature` toolbox for MATLAB from SourceForge:
    [https://sourceforge.net/projects/clifford-multivector-toolbox/](https://sourceforge.net/projects/clifford-multivector-toolbox/)
2.  Extract the downloaded archive (e.g., a `.zip` or `.tar.gz` file) to a directory on your computer.
3.  Open MATLAB.
4.  Add the extracted directory (and its subdirectories) to the MATLAB path. You can do this in several ways:
    * **Using the MATLAB UI:** Go to the "Home" tab, click "Environment," and then "Set Path." Click "Add Folder with Subfolders" and select the directory where you extracted the toolbox. Save the changes.
    * **Using the command line:** In the MATLAB command window, navigate to the extracted directory and use the `addpath(genpath('.'))` command. You might want to add this command to your `startup.m` file to make it persistent across MATLAB sessions.

## Usage

### MATLAB

1.  Navigate to the `MATLAB/` directory.
2.  Open MATLAB and run the `.mlx` files, to view the results.

### Qiskit

1.  Navigate to the `Qiskit/` directory.
2.  Run the Python scripts from your terminal:
    ```bash
    python sud2x3.py
    ```
2.  Open and run the Jupyter notebooks (e.g., `sudoku2_2.ipynb`) to explore the quantum counting approach.

## Author

* [Deepthy Saji]
* [Brno University of Technology]
