# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 20:09:37 2018

@author: murray
"""

# Global vars 
watervel = 1500.0
num_t_samples = 10000 # should be 19000, given a 0.0002 second sample rate and 19s seis line.  
bathyfilename="jc007_EM120_an_bathy13-14_profile.txt"

# Import dependencies 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# Make fake linear seafloor. Will replace with real seafloor later. 
#seaf = np.linspace(2000,2200, num_shotpoints)
seaf = np.genfromtxt(fname=bathyfilename)
seaf = seaf.astype(int)
num_shotpoints = seaf.shape[0]

# make matrix to hold vel model.
mat = np.ones((num_t_samples, num_shotpoints))

# Define seafloor velocity profile 
func = np.ones((2000))
func[0:700] = np.linspace(watervel, 6000,700)
func[700:] = np.linspace(6000, 8000,len(func) - 700)
func = pd.rolling_mean(func, 101, min_periods=1)

# Build matrix
print("Building velocity model....")
for i in range(mat.shape[1]):    
    mat[0:seaf[i,2], i] = watervel
    mat[seaf[i,2]:seaf[i,2]+len(func), i] = func
    mat[seaf[i,2]+len(func):-1, i] = np.max(func)

print(mat.shape)
#np.savetxt(fname="vel_model.txt", X=mat)
print("Finished building model. Making fig...")

# Plot matrix to sanity check
plt.figure(figsize=(5, 8), dpi=50, facecolor='w', edgecolor='k')
plt.imshow(mat)
plt.colorbar()
plt.tight_layout()
plt.savefig("vel_model.jpg")
plt.show()
