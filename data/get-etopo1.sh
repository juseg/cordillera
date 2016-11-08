#!/bin/bash

url="http://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/bedrock/\
cell_registered/georeferenced_tiff/ETOPO1_Bed_c_geotiff.zip"
archive=$(basename $url)
input=${archive%.zip}.tif
output=etopo1.nc

# download archive
[ -f $archive ] || wget $url

# inflate archive
[ -f $input ] || unzip $archive

# reproject for North America
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3979 \
         -te -4250000 -1200000 4250000 3800000 \
         -tr 5000 5000 \
         -wm 512 -wo SOURCE_EXTRA=1000 \
         -srcnodata -2147483648 -dstnodata -2147483648 \
         -of netcdf -overwrite \
         $input etopo1-northamerica.nc

# reproject for the Cordillera (used -tr 3000 3000 for cycle paper)
#proj='+proj=lcc +lon_0=-95 +lat_0=49 +lat_1=79 +lat_2=77'  # cal
proj='+proj=lcc +lon_0=-135 +lat_0=45 +lat_1=45 +lat_2=70'
gdalwarp -s_srs EPSG:4326 -t_srs "$proj" \
         -te -2250000 000000 2250000 3000000 \
         -tr 2500 2500 \
         -wm 512 -wo SOURCE_EXTRA=1000 \
         -srcnodata -2147483648 -dstnodata -2147483648 \
         -of netcdf -overwrite \
         $input etopo1-cordillera.nc
