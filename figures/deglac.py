#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, Normalize
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
topg = nc.variables['topg']

# compute deglaciation age
print 'computing deglaciation age...'
deglacage = np.ones_like(mask[0].T)*120.0
for i, t in enumerate(time[:]/ka):
    print '[ %02.1f %% ]\r' % (100.0*i/len(time)),
    deglacage = np.where(mask[i].T == 2, -t, deglacage)

# plot
ages = [0, 8, 10, 12, 14, 16, 18, 20, 22, 80]
im = ax.imshow(topg[0].T, cmap='Greys', norm=Normalize(-3000, 6000))
cs = ax.contourf(deglacage, levels=ages, cmap='Reds_r', alpha=0.75,
                  norm=BoundaryNorm(ages, 256))
ax.contour(deglacage, levels=ages, colors='k', linewidths=0.2)

# add colorbar and save
cb = fig.colorbar(cs, ax.cax, ticks=ages)
cb.set_label('Deglaciation age (kyr)')
fig.savefig('deglac.png')
nc.close()
