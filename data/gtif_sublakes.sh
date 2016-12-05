#!/bin/bash

# parameters
method=bicubic

# make directory or update modification date
mkdir -p processed
touch processed
cd processed

# import high-resolution topography and set region to it
ifile="../external/cded250k.tif"
g.remove -f type=rast name=cded250k --q
r.in.gdal input=$ifile output=cded250k --q
g.region rast=cded250k

# import and resample boot topography
ifile="cordillera-etopo1bed-5km-boottopo.tif"
g.remove -f type=rast name=boottopo --q
r.in.gdal input=$ifile output=boottopo --q
r.resamp.interp input=boottopo output=boottopo method=$method --q --o

# compute difference
r.mapcalc "topodiff = cded250k - boottopo" --q --o

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
        r.mapcalc "wattable = wattable + 0.09*topodiff" --q --o

        # fill topo until fully resolved
        fillcmd="r.fill.dir output=lakefill direction=flowdirs --o"
        fillout=$($fillcmd input=wattable 2>&1)
        while [ "$(grep unresolved <<< "$fillout" | wc -l)" -gt "1" ]
        do
            grep unresolved <<< "$fillout" | tail -n 1
            fillout=$($fillcmd input=lakefill 2>&1)
        done

        # compute subglacial lake depths
        r.mapcalc "sublakes = lakefill - wattable" --q --o
        r.mapcalc "sublakes = if(sublakes>9999, 0, sublakes)" --q --o

        # mask cold-based areas
        ifile="${prefix}-warmbase-${age}a.tif"
        g.remove -f type=rast name=warmbase --q
        r.in.gdal input=$ifile output=warmbase --q
        r.mapcalc "sublakes = warmbase * sublakes" --q --o

        # output to geotiff
        createopt="compress=deflate"
        r.out.gdal input=sublakes output=$ofile createopt=$createopt -c --q --o

    done

    # create zip archive
    ifile=${prefix}-sublakes-*a.tif
    ofile=${prefix}-sublakes.zip
    [ -f $ofile ] && rm $ofile
    echo "Preparing $ofile ..."
    zip $ofile $ifile -q
done
