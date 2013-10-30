#!/bin/bash

vars=lat,lon,topg,thk,usurf,csurf

# final output and timeseries
for clim in wcnn erai narr cfsrs7 cfsr ncar; do
  for cool in $(seq -f %02g 00 10); do
    atm=cordillera-$clim-10km-bl
    run=pism/output/$atm/stepcool${cool}sll120+ccli+till1030/y0010000
    file=$clim-$cool.nc
    [ ! -f $file ] \
      && ssh scooter "ncks -O -v $vars $run.nc /tmp/$file" \
      && scp scooter:/tmp/$file .
    file=$clim-$cool-ts.nc
    [ ! -f $file ] \
      && scp scooter:$run-ts.nc $file
  done
done

# NARR extra files
for cool in $(seq -f %02g 00 15); do
    atm=cordillera-narr-10km-bl
    run=pism/output/$atm/stepcool${cool}sll120+ccli+till1030/y0010000
    file=narr-$cool-extra.nc
    [ ! -f $file ] \
      && ssh scooter "ncks -O -v $vars $run-extra.nc /tmp/$file" \
      && scp scooter:/tmp/$file .
done

# hybrid atmospheres final output
for clim in erai narr cfsr ncar; do
  for biclim in twcnnp${clim} t${clim}pwcnn; do
    atm=cordillera-$biclim-10km-bl
    run=pism/output/$atm/stepcool05sll120+ccli+till1030/y0010000
    file=$biclim-05.nc
    [ ! -f $file ] \
      && ssh scooter "ncks -O -v $vars $run.nc /tmp/$file" \
      && scp scooter:/tmp/$file .
    file=$biclim-05-ts.nc
    [ ! -f $file ] \
      && scp scooter:$run-ts.nc $file
  done
done
