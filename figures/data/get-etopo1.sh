#!/bin/bash

url="http://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/bedrock/\
grid_registered/georeferenced_tiff/ETOPO1_Bed_g_geotiff.zip"
archive=$(basename $url)
input=${archive%.zip}.tif
output=etopo1.nc

# download archive
[ -f $archive ] || wget $url

# inflate archive
[ -f $input ] || unzip $archive

# reproject
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3979 \
         -te -4250000 -1200000 4250000 3800000 \
         -tr 7500 7500 \
         -wm 512 -wo SOURCE_EXTRA=1000 \
         -srcnodata -2147483648 -dstnodata -2147483648 \
         -of netcdf -overwrite \
         $input $output
