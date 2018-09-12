# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 20:09:37 2018

@author: murray
"""

import numpy as np 
import matplotlib.pyplot as plt

watervel = 1500.0
num_t_samples = 4000
num_shotpoints = 4000


seaf = np.linspace(2000,2200, num_shotpoints)
seaf = seaf.astype(int)
mat = np.ones((num_t_samples, num_shotpoints))
func = 4000 + np.arange(500)*500

for i in range(mat.shape[1]):    
    mat[0:seaf[i], i] = watervel
    mat[seaf[i]:seaf[i]+len(func), i] = func
    mat[seaf[i]+len(func):-1, i] = np.max(func)
        

plt.imshow(mat)
plt.colorbar()
plt.show()

mat.shape



temp = np.ones((40,200))
temp[1,199]
plt.imshow(temp)
plt.show()