#!/bin/bash

# make directory or update modification date
mkdir -p external
touch external
cd external

# Dyke (2003) deglaciation shapefiles
orig=http://ftp.geogratis.gc.ca/pub/nrcan_rncan/publications/ess_sst\
/214/214399/of_1574.zip
dest=dyke-2003.zip
[ -f "$dest" ] || wget $orig -O $dest
unzip -jn $dest data/shp/ice{18..14}k.???
chmod 644 ice{18..14}k.???

# Ehlers et al. (2011) LGM outline
orig=http://static.us.elsevierhealth.com/ehlers_digital_maps/\
digital_maps_02_all_other_files.zip
dest=ehlers-etal-2011.zip
[ -f "$dest" ] || wget $orig -O $dest
unzip -jn $dest lgm.??? lgm_alpen.???

# Ehlers et al. (2011) simplified
ogr2ogr -where "OGR_GEOM_AREA > 1e-3" -simplify 0.1 \
        -overwrite lgm_simple.shp lgm.shp
ogr2ogr -where "OGR_GEOM_AREA > 1e-3" -simplify 0.1 \
        -append lgm_simple.shp lgm_alpen.shp

# ETOPO1 Bed original cell-registered data
orig=http://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/bedrock/\
cell_registered/georeferenced_tiff/ETOPO1_Bed_c_geotiff.zip
dest=etopo1-world.tif
if [ ! -f "$dest" ]
then
    wget $orig -O ${dest%.tif}.zip
    unzip -n ${dest%.tif}.zip
    rm ${dest%.tif}.zip
fi

# ETOPO1 reprojection for North America
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3979 -r bilinear \
         -te -4250000 -1200000 4250000 3800000 -tr 5000 5000 \
         -srcnodata -2147483648 -dstnodata -32768 \
         -wm 512 -wo SOURCE_EXTRA=100 -of netcdf -overwrite \
         etopo1-world.tif etopo1-northamerica.nc

# ETOPO1 reprojection for the Cordillera (used -tr 3000 3000 in cycle paper)
proj="+proj=lcc +lon_0=-135 +lat_0=45 +lat_1=45 +lat_2=70"
gdalwarp -s_srs EPSG:4326 -t_srs "$proj" -r bilinear \
         -te -2250000 000000 2250000 3000000 -tr 2500 2500 \
         -srcnodata -2147483648 -dstnodata -32768 \
         -wm 512 -wo SOURCE_EXTRA=100 -of netcdf -overwrite \
         etopo1-world.tif etopo1-cordillera.nc

# Canada digital elevation data (CDED) 250k
root=ftp://ftp.geogratis.gc.ca/pub/nrcan_rncan/elevation/geobase_cded_dnec
for sector in 0{8..9}{2..3}
do
    ifile=$root/250k_dem/$sector
    ofile=cded250k/$sector
    [ -d $ofile ] || wget -r -nd $ifile -P $ofile
    for f in cded250k/$sector/*.zip
    do
        unzip -n $f '*.dem' -d cded250k
    done
done

# CDED mosaic vrt
gdalbuildvrt cded250k.vrt cded250k/*.dem

# CDED reprojection (epsg 3979 or 7254?)
gdalwarp -t_srs EPSG:3979 -r bilinear \
         -te -1900000 500000 -1700000 650000 -tr 100 100 \
         -srcnodata -32767 -dstnodata -32767 \
         -wm 512 -wo SOURCE_EXTRA=100 -overwrite \
         cded250k.vrt cded250k.tif

# CDED remove unzipped files
rm cded250k/*.dem

# Paleoclimate time series
root=ftp://ftp.ncdc.noaa.gov/pub/data/paleo/
orig=$root/icecore/antarctica/epica_domec/edc3deuttemp2007.txt
dest=epica.txt
[ -f "$dest" ] || wget $orig -O $dest
orig=$root/contributions_by_author/lisiecki2005/lisiecki2005.txt
dest=lr04.txt
[ -f "$dest" ] || wget $orig -O $dest
# additional sea-level data sources
# orig=$root/contributions_by_author/lea2002/lea2002.txt
# orig=$root/contributions_by_author/siddall2003/siddall2003.txt

# ERA40 temperature standard deviation
geodata=ogive:/scratch_net/ogive_second/juliens/geodata
orig=$geodata/reanalysis/era40/era40.sat.mon.5801.std.nc
dest=$(basename $orig)
[ -f "$dest" ] || scp $orig $dest
