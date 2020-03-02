# Sythetic ocean velocity model
This set of scripts creates a synthetic velocity model for oceanic crust, based on a bathymetry profile. 

Note in this version input files are hardcoded (paticularly in vel_extract.sh) due to their being a small number of input files, and anomalies in a number of the data files. Scripts are well commented and should be easily modifiable. 

## Usage
1. First, extract bathymetric profiles - `./vel_extract.sh`
2. Second, create interval velocity models - `./vel_model.py`
3. Third, convert interval velocity to root mean square (RMS) velocity - `./vel_model_int_to_rms.sh`
4. Finally (and optionally), create nmo par files for usage in Seismic Un*x - `./nmo_par_gen.py`

## Dependencies
* Bash
* Generic Mapping Tools
* python3
* numpy
