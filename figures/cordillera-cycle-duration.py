#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from iceplot import plot as iplt

# file path
extra_file = '/home/julien/pism/output/cordillera-narr-6km-bl/' \
             '%scool580+pddc+pddref00+mt8+lc+nofloat+part' \
             '+gflx70+ssa+pp+nfrac02+till1545/full-extra.nc'

# initialize figure
mm = 1/25.4
fig = iplt.gridfigure((62.5, 125), (1, 1), axes_pad=2.5*mm,
                      cbar_mode='single', cbar_pad=2.5*mm, cbar_size=5*mm)
ax = plt.axes(fig.grid[0])

# load extra output and compute duration of ice cover
nc = Dataset(extra_file % 'grip')
icecover = (nc.variables['mask'][:] == 2).sum(axis=0).T
icecover *= 120.0/len(nc.variables['time'])

# plot
levels = range(10,121,10)
im = iplt.bedtopoimage(nc, 0, cmap='Greys', norm=Normalize(-3000, 6000))
cf = ax.contourf(icecover, levels=[1e-6]+levels, cmap='Blues', alpha=0.75)
ax.contour(icecover, levels, colors='k', linewidths=0.2)
ax.contour(icecover, [1e-6], colors='k', linewidths=1.0)

# add colorbar and save
cb = fig.colorbar(cf, ax.cax)
cb.set_label('Duration of ice cover (kyr)')
fig.savefig('cordillera-cycle-duration.png')
nc.close()
