#!/bin/bash

vars=lat,lon,topg,thk,usurf,csurf

# input basal topography
file=etopo1bed.nc
[ ! -f $file ] \
  && scp scooter:pism05/input/boot/cordillera-etopo1bed-10km.nc $file

# input atmosphere files
for clim in 'wc' wcnn erai narr cfsrs7 cfsr ncar; do
  for int in nn bl; do
    atm=cordillera-$clim-10km-$int
    file=$clim-$int.nc
    [ ! -f $file ] \
      && scp scooter:pism05/input/atm/$atm.nc $file
  done
done

# final output and timeseries
for clim in wcnn erai narr cfsrs7 cfsr ncar; do
  for cool in $(seq -f %02g 00 10); do
    atm=cordillera-$clim-10km-bl
    run=pism05/output/$atm/stepcool${cool}sll120+ccli+till1030/y0010000
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
    run=pism05/output/$atm/stepcool${cool}sll120+ccli+till1030/y0010000
    file=narr-$cool-extra.nc
    [ ! -f $file ] \
      && ssh scooter "ncks -O -v $vars $run-extra.nc /tmp/$file" \
      && scp scooter:/tmp/$file .
done

# hybrid atmospheres final output
for clim in erai narr cfsr ncar; do
  for biclim in twcnnp${clim} t${clim}pwcnn; do
    atm=cordillera-$biclim-10km-bl
    run=pism05/output/$atm/stepcool05sll120+ccli+till1030/y0010000
    file=$biclim-05.nc
    [ ! -f $file ] \
      && ssh scooter "ncks -O -v $vars $run.nc /tmp/$file" \
      && scp scooter:/tmp/$file .
    file=$biclim-05-ts.nc
    [ ! -f $file ] \
      && scp scooter:$run-ts.nc $file
  done
done
