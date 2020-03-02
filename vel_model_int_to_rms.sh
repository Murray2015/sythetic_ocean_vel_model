#!/bin/bash

##### This script runs after vel_model.py but before nmo_par_gen.py. It takes the x,y,IntVel file from vel_mode.py.
##### This converts seismic interval velocities created by vel_model.py into RMS velocities.

vel_mod=vel_model_L1.1_downsamp_y_x_vint.txt

# Find sample rate
SR=`head ${vel_mod} -n2 | awk 'BEGIN{first=0.0; last=0.0}{last=first;first=$1}END{print first-last}'`
echo $SR

# Make new folder
dir_name=`echo $vel_mod | awk -F"_" '{print $3}'`
mkdir -p $dir_name
cp $vel_mod ${dir_name}/${vel_mod}
cd $dir_name

# Split vel model into 1 file per trace
cat vel_model_L1.1_downsamp_y_x_vint.txt | awk '{print >$2".txt"}'

# Remove old master file
rm ${vel_mod}_master.txt

# Loop over each tract file
for i in `ls -v *0.txt`
do
# Find number of samples
ns=`wc $i | awk '{print $1}'`
echo $ns
# Convert velocities
echo $i, $SR, $ns
awk '{print $3}' $i > temp
a2b n1=1 < temp > ${i}.b
velconv intype=vintt outtype=vrmst dt=$SR nt=$ns ft=0.0 < ${i}.b | b2a n1=1 > ${i}.RMS.txt
paste ${i} ${i}.RMS.txt > ${i}.INT.RMS.txt
cat ${i}.INT.RMS.txt >> ${vel_mod}_master.txt
done

# Clean up binary and aux text files
rm *.b temp *00.txt *txt.RMS*

exit
