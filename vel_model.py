# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 20:09:37 2018

@author: murray
"""
# Global vars 
watervel = 1500.0
num_t_samples = 6000
num_shotpoints = 7000


# Import dependencies 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

# Make fake linear seafloor. Will replace with real seafloor later. 
seaf = np.linspace(2000,2200, num_shotpoints)
seaf = seaf.astype(int)

# make matrix to hold vel model.
mat = np.ones((num_t_samples, num_shotpoints))

# Define seafloor velocity profile 
func = np.ones((2000))
func[0:700] = np.linspace(watervel, 6000,700)
func[700:] = np.linspace(6000, 8000,len(func) - 700)
func = pd.rolling_mean(func, 101, min_periods=1)

# Build matrix
for i in range(mat.shape[1]):    
    mat[0:seaf[i], i] = watervel
    mat[seaf[i]:seaf[i]+len(func), i] = func
    mat[seaf[i]+len(func):-1, i] = np.max(func)
        
# Plot matrix to sanity check
plt.imshow(mat)
plt.colorbar()
plt.show()