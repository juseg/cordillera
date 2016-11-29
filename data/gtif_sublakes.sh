#!/bin/bash

# parameters
#reg=cordillera
#res=1000
method=bicubic

# make directory or update modification date
mkdir -p processed
touch processed
cd processed

# set region and resolution
#g.region region=$reg res=$res
g.region w=-2300000 e=-1500000 s=300000 n=900000 res=500

# expand region by half a grid cell
wesn=($(g.region -t | tr '/' ' '))
w=${wesn[0]}
e=${wesn[1]}
s=${wesn[2]}
n=${wesn[3]}
g.region w=$((w-res/2)) e=$((e+res/2)) s=$((s-res/2)) n=$((n+res/2))

# reproject high-res topo
r.proj location=world-ll-wgs84 input=etopo1bed method=$method --q --o

# import and resample boot topography
ifile="cordillera-etopo1bed-5km-boottopo.tif"
g.remove -f type=rast name=boottopo --q
r.in.gdal input=$ifile output=boottopo --q
r.resamp.interp input=boottopo output=boottopo method=$method --q --o

# loop on geoflux maps
for ghf in gou11simi
do
    prefix="cordillera-narr-5km-grip3222cool620+cgeo1+till1545+${ghf}"

    # loop on model age
    for age in 19100
    do

        # filenames
        ifile="${prefix}-wattable-${age}a.tif"
        ofile="${prefix}-sublakes-${age}a.tif"
        echo "Preparing $ofile ..."

        # import and resample water table
        g.remove -f type=rast name=wattable --q
        r.in.gdal input=$ifile output=wattable --q
        r.resamp.interp input=wattable output=wattable method=$method --q --o

        # compute hi-res water table
        r.mapcalc "topodiff = etopo1bed - boottopo" --q --o
        r.mapcalc "wattable = wattable + 0.09*topodiff" --q --o

        # compute subglacial lake depths
        r.fill.dir input=wattable output=lakefill direction=flowdirs --q --o
        r.mapcalc "sublakes = lakefill - wattable" --q --o

        # output to geotiff
        r.out.gdal input=sublakes output=$ofile createopt="COMPRESS=DEFLATE" -c --q --o

    done

    # create zip archive
    ifile=${prefix}-sublakes-*a.tif
    ofile=${prefix}-sublakes.zip
    [ -f $ofile ] && rm $ofile
    echo "Preparing $ofile ..."
    zip $ofile $ifile -q
done
