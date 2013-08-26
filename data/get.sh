#!/bin/bash

# download and strip data files from scooter
for clim in wcnn erai narr cfsrs7 cfsr ncar; do
  for cool in $(seq -f %02g 00 10); do
    atm=cordillera-$clim-10km-bl
    run=pism/output/$atm/stepcool${cool}sll120+ccli+till1030/y0010000
    if [ ! -f $clim-$cool.nc ]; then
      ssh scooter "ncks -O -v lat,lon,topg,thk,usurf,csurf $run.nc /tmp/tmp.nc"
      scp scooter:/tmp/tmp.nc $clim-$cool.nc
    fi
    if [ ! -f $clim-$cool-ts.nc ]; then
      scp scooter:$run-ts.nc $clim-$cool-ts.nc
    fi
  done
done

