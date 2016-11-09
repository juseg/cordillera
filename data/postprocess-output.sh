#!/bin/bash

# output dir and variables to include
odir="$HOME/pism/output/0.7.2/cordillera-narr-5km"
vars="lon,lat,bwat,bmelt,thk"

# config and geoflux arguments
confargs=( "cgeo1+hynull" "cgeo1" "cgeo1" "cgeo1" "cgeo1" "cgeo1" )
gflxargs=( "" "" "+dav13" "+gou11comb" "+gou11simi" "+sha04" )

# make directory or update modification date
mkdir -p processed
touch processed
cd processed

# for each of the six runs
for i in {0..5}
do

    # get run name
    conf=${confargs[i]}
    gflx=${gflxargs[i]}
    runname="grip3222cool620+${conf}+till1545${gflx}"

    # compute sum
    echo "processing $runname ..."
    ifile="$odir/$runname/y???????-extra.nc"
    ofile="$runname.avg.nc"
    ncra -O -d time,,,1 -v $vars $ifile $ofile

done
