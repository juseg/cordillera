#!/bin/bash

# output dir and variables to include
odir="$HOME/pism/output/0.7.2/cordillera-narr-5km"
vars="lon,lat,thk,topg,usurf,temppabase,velbase_mag"

# records and offsets
records=( grip epica )
offsets=( 620 590 )

# make directory or update modification date
mkdir -p processed
touch processed
cd processed

# for each record
for i in {0..1}
do

    # file names
    rec=${records[i]}
    dt=${offsets[i]}
    ifile="$odir/${rec}3222cool${dt}+ccyc4+till1545/y???????-extra.nc"
    ofile="cordillera-cycle-${rec}-deglacvars.nc"

    # compute sum
    echo "preparing $ofile ..."
    ncrcat -O -d time,1039,1099,10 -v $vars $ifile $ofile

done
