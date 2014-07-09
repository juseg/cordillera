#!/usr/bin/env python2
# coding: utf-8

"""Plot effect of PDD standard deviation."""

import sys

sys.path.append('iceplot')

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import plot as iplt
from iceplot import cm as icm
pism_dir = '/home/julien/pism06/'

# plot standard deviation effect
fig = iplt.gridfigure((30.0, 60.0), (1, 4), cbar_mode='single',
    axes_pad=2.5/25.4, cbar_pad=2.5/25.4, cbar_size=5/25.4)

# loop
for i, sdargs in enumerate(['+sd0', '+sd3', '', '+sdp']):
    print sdargs
    ax = plt.axes(fig.grid[i])
    nc = Dataset('/home/julien/pism/output/cordillera-narr-10km-bl/'
                 'stepcool07sll120+ccyc+till1545%s/y0010000.nc' % sdargs)
    im = iplt.icemap(nc, 0)
    nc.close()

# add colorbar and save
cb = fig.colorbar(im, fig.grid.cbar_axes[0])
cb.set_label(r'ice surface velocity ($m\,a^{-1}$)')
fig.savefig('plot-sdeffect.png')
