#!/bin/bash 

bathyfile=jc007_EM120_and_bathy13-14.grd
coords=L6a.26.su_geom
stem=`echo $bathyfile | tr -d .grd`

grdtrack $coords -G$bathyfile | sort -k1 | uniq > temp.txt
sample1d temp.txt -Ar -Fl -T6.25e > ${stem}_profile.txt
rm temp.txt
