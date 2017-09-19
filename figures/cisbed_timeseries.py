#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
from matplotlib.animation import FuncAnimation

# initialize figure
fig, tsax = ut.pl.subplots_mm(1, 1, figsize=(170.0, 60.0),
                              left=10.0, right=10.0, bottom=7.5, top=2.5,
                              hspace=2.5, wspace=2.5)
twax = tsax.twinx()

# load boot topo
filepath = 'input/boot/cordillera-etopo1bed+thk+gou11simi-10km.nc'
nc = ut.io.load(filepath)
zref = nc.variables['topg'][:].T
nc.close()

# for each record
for i, rec in enumerate(ut.cisbed_records):
    c = ut.cisbed_colours[i]
    dt = ut.cisbed_offsets[i]
    dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))

    # for each configuration
    cisbed_configs = ['', '+num1e21']  # FIXME move to util
    cisbed_lstyles = ['-', ':']  # FIXME move to util
    for j, conf in enumerate(cisbed_configs):
        ls = cisbed_lstyles[j]
        run_dir = ('output/e9d2d1f/cordillera-narr-10km/'
                   '%s+cisbed2%s+till1545'% (dt_file, conf))

        # load ice volume time series
        nc = ut.io.load(run_dir + '/y???????-ts.nc')
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)
        vol = nc.variables['slvol'][:]
        nc.close()

        # plot ice volume time series
        tsax.plot(age, vol, c=c, ls=ls, alpha=0.25)

        # load bedrock topography
        nc = ut.io.load(run_dir + '/y???????-extra.nc')
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        z = nc.variables['topg'][:]
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)

        # plot bedrock depression time series
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        dep = (zref-z).sum(axis=(1, 2))*dx*dy*1e-12
        twax.plot(age, dep, c=c, ls=ls)

# set time series axes properties
tsax.set_xlim(120.0, 0.0)
tsax.set_ylim(-0.5, 9.5)
tsax.set_xlabel('model age (ka)')
tsax.set_ylabel('ice volume (m s.l.e.)', color='0.75')
tsax.tick_params(axis='y', colors='0.75')
tsax.grid(axis='y')

# set twin axes properties
twax.set_ylim(-50.0, 950.0)
twax.set_ylabel('volumic depression ($10^{3}\,km^{3}$)')

# save preview
ut.pl.savefig(fig)
