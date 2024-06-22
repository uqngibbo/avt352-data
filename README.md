# avt352-data

This repository contains the data of the cone-flare simulations to be used for postprocessing. There are three main folders as shown below

```bash
.
├── cfddata
├── python_scripts
└── refdata
```

- cfddata: folder containing the CFD predictions obtained by the participants
- python_scripts: postprocessing scripts
- refdata: contains the experimental data

## cfddata
This folder has a set structure **which should be followed**. Each participant has a set folder, if not present please add it. 

```bash
.
├── ansys_aselsan
├── ansys_inc
├── cadence
├── coda
├── eilmer
├── gaspex
├── h3amr
├── overflow
├── starccm
├── SU2
└── tau
```

Withing this folder, the following subfolder structure should be used with *geom1* referring to the 6/42 degree case and *geom2* referring to the 7/40 degree case. In the respective geometry folders, run number folders must be used. **Note: only add run folders when you do have data**

```
.
├── geom1
│   └── run4
└── geom2
    ├── run14
    ├── run28
    ├── run33
    ├── run34
    ├── run37
    ├── run41
    └── run45
```

The filenames should also follow a given order. For example in run45 folder this should be as shown below. It follows the naming separated by "_" RUN_NB  + VARIABLE +  MESH_NB  and the turbulence model separated by "-".  This naming is used in the postprocessing script. It can be an internal naming convention as later on the keywords are used to be replaced by whatever you desire. For instance ```_meshXXX-SSTa10355_Prt086Lemmon``` which refers to a specific grid and a specific turbulence model setting.

```
run45
├── run45_wallHeatFlux_mesh06-SST.csv
├── run45_wallHeatFlux_mesh07-SST.csv
├── run45_wallHeatFlux_mesh08-SST.csv
├── run45_wallHeatFlux_mesh09-SST.csv
├── run45_wallHeatFlux_meshXXX-SSTa10355_Prt086Lemmon.dat
├── run45_wallP_mesh06-SST.csv
├── run45_wallP_mesh07-SST.csv
├── run45_wallP_mesh08-SST.csv
└── run45_wallP_mesh09-SST.csv
```

## python_scripts
Various scripts used to do postprocessing. The helper_functions.py are used in the other scripts and contain generic functions to read the data from the various participants.

```python_scripts/
├── analyse_holden_data_generic.py
├── compare_holden_data.py
├── compute_separation_peak.py
├── helper_functions.py
```

```analyse_holden_data_generic.py``` allows the user to compare his simulation results of interest to the experiments, as well as compare various grids. 
```compare_holder_data.py``` is used to create comparative plots between participants.

### NOTE: **the experimental data of the 6/42 run 4 case is automatically transformed to the streamwise axial position when loaded! No need to retransfrom the data. NEED TO CHECK IF ALSO REQUIRED FOR run 6?**


## refdata
Folder with experimental data structured as follows

```refdata/
├── run14_heatFlux.csv
├── run14_pressure.csv
├── run28_heatFlux.csv
├── run28_pressure.csv
├── run33_heatFlux.csv
├── run33_pressure.csv
├── run34_heatFlux.csv
├── run34_pressure.csv
├── run37_heatFlux.csv
├── run37_pressure.csv
├── run41_heatFlux.csv
├── run41_pressure.csv
├── run45_heatFlux.csv
├── run45_pressure.csv
├── run4_heatFlux.csv
├── run4_pressure.csv
├── run6_heatFlux.csv
└── run6_pressure.csv
```