#!/bin/bash

# download and strip data files from scooter
for clim in wcnn erai narr cfsrs7 cfsr ncar; do
  for cool in $(seq -f %02g 00 09); do
    if [ ! -f $clim-$cool.nc ]; then
      ssh scooter "ncks -O -v topg,thk,usurf,csurf pism/output/cordillera-$clim-10km-bl/stepcool${cool}sll120+ccli+till1030/y0010000.nc /tmp/tmp.nc"
      scp scooter:/tmp/tmp.nc $clim-$cool.nc
    fi
  done
done

