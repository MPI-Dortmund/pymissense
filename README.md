[![DOI](https://zenodo.org/badge/697276360.svg)](https://zenodo.org/badge/latestdoi/697276360)

# pymissense
PyMissense creates the pathogencity plot and modified pdb as shown in the [AlphaMissense paper](https://www.science.org/doi/10.1126/science.adg7492) for custom proteins.

## What it does

AlphaMissense allows you to identify regions in your amino acid chain that are critical for protein function. This skript does two things:

1. It generates a plot similar to [Figure 3D](https://www.science.org/doi/10.1126/science.adg7492#F3) of the [AlphaMissense paper](https://www.science.org/doi/10.1126/science.adg7492)

   <img src="resources/img/3d.png" width="400">



2. It creates a modified PDB file where the temperature factor is replaced by the pathogencity predicted by AlphaMissense that allows you to visualize the effect with Chimerax, like [Figure 3E](https://www.science.org/doi/10.1126/science.adg7492#F3) of the paper:

   <img src="resources/img/3e.jpeg" width="400">

It does so by replacing the bfactor in the PDB.

## How to install

```
pip install pymissense
```
    
## How to use it

Generate usage is:
```
usage: pymissense [-h] [--pdbpath PDBPATH] [--maxacid MAXACID] uniprot_id output_path

AlphaMissense plot and pdb generator

positional arguments:
  uniprot_id         UNIPROT ID
  output_path        Output folder

options:
  -h, --help         show this help message and exit
  --pdbpath PDBPATH  If defined, it will write the pathogencity as bfactor in that PDB. If its not defined or not existing it will instead download the alphafold predicted PDB (default: None)
  --maxacid MAXACID  Maximum squence number to use. (default: None)
```

You can provide the optional argument `--pdbpath` if you want to use an experimental PDB, otherwise it will instead download the alphafold predicted PDB.

For example, to reproduce [Figure 3D](https://www.science.org/doi/10.1126/science.adg7492#F3) (the middle one) and the generate the PDB shown in [Figure 3E](https://www.science.org/doi/10.1126/science.adg7492#F3) do:

```
wget https://files.rcsb.org/download/7UPI.pdb
pymissense Q9UQ13 out --maxacid 200 --pdbpath 7upi.pdb 
```

Note that they displayed only the first 200 amino acids in the plots and showed the pathogencity with the experimental PDB `7upi`.

## Contributions

This script was developed in collaboration with Tobias Raisch 