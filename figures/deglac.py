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

# unit conversion
mm = 1/25.4
ka = 365.0 * 24 * 60 * 60 * 1000

# initialize figure
fig = iplt.gridfigure((62.5, 125), (1, 1), axes_pad=2.5*mm,
                      cbar_mode='single', cbar_pad=2.5*mm, cbar_size=5*mm)
ax = plt.axes(fig.grid[0])

# read extra output
print 'reading extra output...'
nc = Dataset(extra_file % 'grip')
time = nc.variables['time']
mask = nc.variables['mask']

# compute deglaciation age
print 'computing deglaciation age...'
deglacage = np.ma.masked_all_like(mask[0].T)
for i, t in enumerate(time[:]/ka):
    deglacage = np.ma.where(mask[i].T == 2, -t, deglacage)

# plot
im = plt.imshow(deglacage, cmap='spectral_r')

# add colorbar and save
cb = fig.colorbar(im, ax.cax)
cb.set_label('Deglaciation age (kyr)')
fig.savefig('deglac.png')
nc.close()
