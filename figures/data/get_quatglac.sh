#!/bin/bash

url="http://static.us.elsevierhealth.com/ehlers_digital_maps/\
digital_maps_02_all_other_files.zip"
archive=$(basename $url)
input=lgm.shp
output=etopo1.nc

# download archive
[ -f $archive ] || wget $url

# inflate archive
# (we need to escape the wildcards to not match already inflated files)
[ -f $input ] || unzip -u $archive ${input%.shp}.\*

# remove small polygons and simplify others
ogr2ogr ${input%.shp}_simple.shp $input -overwrite \
    -where "OGR_GEOM_AREA > 1e-3" -simplify 0.1
