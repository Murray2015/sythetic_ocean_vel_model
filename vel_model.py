# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 20:09:37 2018

@author: Murray Hoggett, murrayhoggett@gmail.com 
"""

# Global vars 
watervel = 1500.0
time_sample_rate = 0.02
record_length_s = 19
bathyfilename="extracted_bathy_profiles/L1.1.su_geom_jc007_EM120_an_bathy13-14_profile.txt"
#outfile=".".join(bathyfilename.split(".")[0:2])
outfile="L1.1"
extract_every_ith_col = 50 # Take every ith column (CDP) of the full vel model. Used for downsampling. 

# Import dependencies 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# Get seafloor from text file   
seaf = np.genfromtxt(fname=bathyfilename)
seaf_t = 2*(abs(seaf[:,2])/1500.0)
seaf = np.append(seaf, np.reshape(seaf_t, (seaf_t.shape[0], 1)), axis=1) # Convert distance into twtt in column [,2] 
num_shotpoints = seaf.shape[0]
num_t_samples = record_length_s / time_sample_rate  
seaf = seaf[::-1]
#plt.plot(seaf[:,2])
#plt.show()

# make matrix to hold vel model.
mat = np.ones((num_t_samples, num_shotpoints))

# Define seafloor velocity profile 
length_func_s = 2
func = np.ones((length_func_s / time_sample_rate))
knee_location = int(len(func) * 0.3)
func[0:knee_location] = np.linspace(watervel, 6000, knee_location)
func[knee_location:] = np.linspace(6000, 8000, len(func) - knee_location)
func = pd.rolling_mean(func, 9, center=True, min_periods=1) # Be aware this introduces an earlier knee in the func. 

print(mat.shape)
print(mat)
print(func) 
print(seaf)
# Build matrix
print("Building velocity model....")
# For each seismic trace 
for i in range(mat.shape[1]):
    # Find the seafloor time in terms of the sample rate
    seaf_time_in_samprate = int(seaf[i,3] / time_sample_rate)
    mat[0:seaf_time_in_samprate, i] = watervel
    mat[seaf_time_in_samprate:seaf_time_in_samprate+len(func), i] = func
    mat[seaf_time_in_samprate+len(func):, i] = np.max(func)

# Downsample by taking every ith column 
outmat = mat[:,::extract_every_ith_col]
print(outmat.shape)
np.savetxt(fname="vel_model_" + outfile + ".txt", X=outmat)

# Try to output as xyz 
m,n = outmat.shape
R,C = np.mgrid[:m,:n]
R = R.astype("float64") * time_sample_rate
C *= extract_every_ith_col
out = np.column_stack((C.ravel(),R.ravel(), outmat.ravel()))
np.savetxt(fname="vel_model_" + outfile + "_downsamp_x_y_vint.txt", X=out, fmt='%f')
# Make a second file with a different ordering
out2 = np.column_stack((R.ravel(order="F"), C.ravel(order="F"), outmat.ravel(order="F")))
np.savetxt(fname="vel_model_" + outfile + "_downsamp_y_x_vint.txt", X=out2, fmt='%f')


print("Finished building model. Making fig...")
# Plot matrix to sanity check
plt.figure(figsize=(16, 8), dpi=50, facecolor='w', edgecolor='k')
plt.imshow(mat, cmap="plasma", aspect="auto", extent=[0,seaf.shape[0],record_length_s,0])
plt.colorbar().set_label("Seismic velocity (m/s)")
#plt.contour(mat, colors="black", aspect="auto", extent=[0,seaf.shape[0],record_length_s,0])
plt.xlabel("Trace number from 0")
plt.ylabel("Time sample number")
plt.tight_layout()
plt.savefig("vel_model.jpg")
plt.show()
