"""
This script makes a par file for sunmo from a xyz (cdp time_location velocity) file. 

Output should look like: 
cdp=1,2,3,4,5,6 tnmo=num,num,num vnmo=num,num,num tnmo=num,num,num vnmo=num,num,num tnmo=num,num,num vnmo=num,num,num tnmo=num,num,num vnmo=num,num,num

"""
vfile="L1.1/vel_model_L1.1_downsamp_y_x_vint.txt_master.txt"

import numpy as np 

# Read file 
print("Reading array from file...")
vel_model_xyz = np.loadtxt(vfile)
print(vel_model_xyz)

# Sort the array 
print("Sorting array...") 
sorted_index_1stcol = np.lexsort((vel_model_xyz[:,0], vel_model_xyz[:,1]))
vel_model_xyz_sort = vel_model_xyz[sorted_index_1stcol]

# Split the array 
array_list = np.split(vel_model_xyz_sort, np.where(np.diff(vel_model_xyz_sort[:,1]))[0]+1)

cdp_string="cdp="
tnmo_vnmo_string = ""

for array in array_list:
	blank_cdp = True
	tnmo_string="tnmo="
	vnmo_string="vnmo="
	for line in array:
		cdp = line[1]
		time = line[0]
		vel = line[3]
		if blank_cdp:
			cdp_string += str(cdp)+","
			blank_cdp = False
		tnmo_string += str(time)+","
		vnmo_string += str(vel)+","
	tnmo_vnmo_string += tnmo_string[:-1] + " " + vnmo_string[:-1] + " "

output_string = cdp_string[:-1] + " " + tnmo_vnmo_string
text_file = open(vfile.split("/")[0] + "_nmo_par.txt", "w")
text_file.write(output_string)
text_file.close()

