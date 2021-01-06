#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib import colors as mcolors
from matplotlib import animation as mani
from iceplot import plot as iplt
from iceplot import cm as icm
from iceplot import animation as iani

# matplotlib settings
mplt.rc('font', size=8)
mplt.rc('mathtext', default='regular')

# unit conversion
mm2in = 1/25.4
s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)
mm = 1/25.4
ka = 365.0 * 24 * 60 * 60 * 1000

# file path
run_path = '/home/julien/pism/output/cordillera-narr-5km-bl/' \
           'grip3222cool580+ccyc+till1545/y0120000'

# drawing function for animations
def draw(t):
    time = nc.variables['time'][t] / ka
    print '%03i, %s ka' % (t, time)

    # draw bed topography and ice margin
    ax = mplt.cla()
    im = iplt.bedtopoimage(nc, t)
    cs = iplt.icemargincontour(nc, t, linewidths=1.0)

    # draw velocity map
    thk = nc.variables['thk'][t].T
    u = nc.variables['uvelsurf'][t].T
    v = nc.variables['vvelsurf'][t].T
    c = np.ma.masked_where(thk < 1, (u**2+v**2)**0.5)
    im = mplt.imshow(c, cmap=icm.velocity,
                     norm=mcolors.LogNorm(10, 10000),
                     alpha=0.5, zorder=1)

    # draw surface topography contours
    cs = iplt.surftopocontour(nc, t, levels=range(200, 6000, 200), linewidths=0.2)
    cs = iplt.surftopocontour(nc, t, levels=range(1000,6000,1000), linewidths=0.5)
    #cs.clabel(fontsize=4, fmt='%g')

    # add label
    mplt.text(275, 575, '%s ka' % time,
        va='top', ha='right',
        bbox=dict(ec='k', fc='w', alpha=1.0, pad=10.0))

# load data
nc = Dataset(run_path + '-extra.nc')

# initialize figure
fig = iplt.simplefigure((40.01, 80.01), axes_pad=0*mm)
mplt.sca(fig.grid[0])

# draw first frame and colorbar
im = draw(0)
#cb = fig.colorbar(im, ax.cax, format='%g')
#cb.set_label('ice surface velocity (m/yr)')

# create animation and save all frames
writer = iani.IceWriter(temp_prefix='animation/frame-', clear_temp=False)
anim = mani.FuncAnimation(fig, draw, 1199)
anim.save('animation.mp4', writer=writer)
nc.close()
