#!/bin/bash 

bathyfile=jc007_EM120_and_bathy13-14.grd
coords=L6a.26.su_geom
stem=`echo $bathyfile | tr -d .grd`

grdtrack $coords -G$bathyfile > ${stem}_profile.txt