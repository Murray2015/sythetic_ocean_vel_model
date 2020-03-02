#!/bin/bash

### This script makes a bathymetry profile for every seismic geometry file located in this directory, and saves it to a folder "extracted_bathy_profiles"

## Set bathymetry file and map projection
bathyfile=jc007_EM120_and_bathy13-14.grd
prj=-JX6i/1i

## Start code
mkdir -p extracted_bathy_profiles

# Loop over input files
for i in `ls *geom`
do
coords=L1.1.su_coords_new.txt
stem=`echo $bathyfile | tr -d .grd`
# Deal with n-s verses e-w
if [[ "$coords" =~ ^(L8.8.su_geom|L11.11.su_geom|L12.12.su_geom|L13.13.su_geom|L14.14.su_geom|L14a.16.su_geom|L15.15.su_geom|L15a.17.su_geom|L16.18.su_geom|L18.20.su_geom|L23.24.su_geom)$ ]];
then
	grdtrack $coords -G$bathyfile | sort -k2 | uniq > temp.txt
	sample1d temp.txt -Ar -Fl -T6.25e > extracted_bathy_profiles/${coords}_${stem}_profile.txt
	rgn=`gmtinfo -I0.05/10 extracted_bathy_profiles/${coords}_${stem}_profile.txt -i1,2`
	psxy $rgn extracted_bathy_profiles/${coords}_${stem}_profile.txt $prj -Bx0.1 -By200 -W1 -i1,2 > extracted_bathy_profiles/${coords}_${stem}.ps
else
	grdtrack $coords -G$bathyfile | sort -k1 | uniq > temp.txt
	sample1d temp.txt -Ar -Fl -T6.25e > extracted_bathy_profiles/${coords}_${stem}_profile.txt
	rgn=`gmtinfo -I0.05/10 extracted_bathy_profiles/${coords}_${stem}_profile.txt -i0,2`
	psxy $rgn extracted_bathy_profiles/${coords}_${stem}_profile.txt $prj -Bx0.1 -By200 -W1 -i0,2 > extracted_bathy_profiles/${coords}_${stem}.ps
fi
# Convert image into jpg
psconvert extracted_bathy_profiles/${coords}_${stem}.ps -A0.5 -P
rm temp.txt
done
eog extracted_bathy_profiles/*jpg
exit
