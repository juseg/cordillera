#!/bin/bash

# output dir and variables to include
odir="/home/juliens/pism/output/0.7.2/cordillera-narr-10km"
vars="lon,lat,bwat,bmelt,thk"

# config and geoflux arguments
confargs=( "cgeo1+hynull" "cgeo1" "cgeo1" "cgeo1" "cgeo1" "cgeo1" )
gflxargs=( "" "" "+dav13" "+gou11comb" "+gou11simi" "+sha04" )

# for each of the six runs
for i in {0..5}
do

    # get file name
    conf=${confargs[i]}
    gflx=${gflxargs[i]}
    runname="grip3222cool620+${conf}+till1545${gflx}"
    ifiles="$odir/$runname/y???????-extra.nc"

    # compute sum in subprocess
    ofile="$runname.avg.nc"
    echo "preparing $ofile..."
    ncra -O -d time,,,1 -v $vars $ifiles $ofile

done
