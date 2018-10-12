# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 20:09:37 2018

@author: Murray Hoggett, murrayhoggett@gmail.com 
"""


# Global vars 
watervel = 1500.0
time_sample_rate = 0.001
record_length_s = 19
num_t_samples = 10000  # should be 95000, given a 0.0002 second sample rate and 19s seis line. 
bathyfilename="jc007_EM120_an_bathy13-14_profile.txt"

# Import dependencies 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# Get seafloor from text file   
seaf = np.genfromtxt(fname=bathyfilename)
seaf_t = 2*(abs(seaf[:,2])/1500.0)
seaf = np.append(seaf, np.reshape(seaf_t, (seaf_t.shape[0], 1)), axis=1) # Convert distance into twtt in column [,2] 
num_shotpoints = seaf.shape[0]

# In future, change this for sample rate 
num_t_samples = 8000 #record_length_s / time_sample_rate  # should be 19000, given a 0.0002 second sample rate and 19s seis line. 

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
    mat[seaf_time_in_samprate+len(func):-1, i] = np.max(func)

print(mat.shape)
np.savetxt(fname="vel_model.txt", X=mat)
print("Finished building model. Making fig...")

# Plot matrix to sanity check
plt.figure(figsize=(16, 8), dpi=50, facecolor='w', edgecolor='k')
plt.imshow(mat, aspect="auto", cmap="inferno")
plt.colorbar().set_label("Seismic velocity (m/s)")
plt.contour(mat, colors="black")
plt.xlabel("Trace number from 0")
plt.ylabel("Time sample")
plt.tight_layout()
#plt.savefig("vel_model.jpg")
plt.show()
