#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplotlib')

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from matplotlib.gridspec import GridSpec
from matplotlib.transforms import blended_transform_factory
from matplotlib.patches import Polygon
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplotlib import plot as iplt

s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)

# analysis functions
def bounded_argmin(a, coord, bmin, bmax):
    return np.ma.argmin(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def bounded_argmax(a, coord, bmin, bmax):
    return np.ma.argmax(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))

# file path
run_path = (os.environ['HOME'] + '/pism/output/0.7.2-craypetsc/cordillera-narr-5km/'
            'grip3222cool620+ccyc4+till1545/y???????')

# read output time series
print 'reading time series...'
nc = iplt.load(run_path + '-ts.nc')
time = nc.variables['time'][:]*s2ka
ivol = nc.variables['slvol'][:]
nc.close()

# locate snapshot times
idxlist = [
    bounded_argmin(ivol, time, -45, -20),
    bounded_argmin(ivol, time, -35, -30),
    bounded_argmin(ivol, time, -30, -25),
    bounded_argmin(ivol, time, -26, -20),
    bounded_argmax(ivol, time, -20, -18),  # LGM
    bounded_argmax(ivol, time, -16, -14),
    10699,  # 13 ka
    bounded_argmax(ivol, time, -12, -10),  # YD
    10999,  # 10 ka
]
tkalist = time[idxlist]
ivolist = ivol[idxlist]
ntka = len(tkalist)

# initialize figure
# wspace = 1/((1+gridw/pad)/npanels-1)
figw, figh = 170.0, 80.0
fig = plt.figure(0, (figw/25.4, figh/25.4))
gs = GridSpec(2, ntka+1, left=2.5/figw, right=1-7.5/figw,
                       bottom=5.0/figh, top=1-2.5/figh,
                       wspace=1/((1+160.0/2.5)/ntka-1),
                       hspace=1/((1+72.5/12.5)/2-1),
                       width_ratios=[6]*ntka+[1])
ax = plt.subplot(gs[0, :])
ax = tsax = plt.subplot(gs[1, :])

# coordinate transformations
blendtrans = blended_transform_factory(tsax.transData, tsax.transAxes)
figinvtrans = fig.transFigure.inverted()

# plot time series
print 'plotting time series...'
ax.plot(time, ivol, color='#1f78b4')  # alt. wiki color #0978ab
ax.set_xlabel('model time (kyr)')
ax.set_ylabel('ice volume (m s.l.e.)')
ax.yaxis.set_ticks_position('right')
ax.yaxis.set_label_position('right')
ax.grid(axis='y', c='0.5', ls='-', lw=0.1)
for tka in tkalist:
    ax.axvline(tka, color='0.5',  lw=0.1)
#ax.plot(tkalist, ivolist, color='#0978ab', marker='+', ls='')  # add crosses

# read extra output
print 'reading extra output...'
nc = iplt.load(run_path + '-extra.nc')
time = nc.variables['time'][:]*s2ka

# plot snapshots
for i, tka in enumerate(tkalist):
    print 'plotting %s ka snapshot...' % tka
    ax = plt.subplot(gs[0, i])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_rasterization_zorder(2.5)

    # find nearest slice
    t = (np.abs(time[:]-tka)).argmin()

    # bed topography
    im = iplt.imshow(nc, 'topg', ax, t)
    iplt.shading(nc, 'topg', ax, t)

    # surface velocity
    im = iplt.imshow(nc, 'velsurf_mag', ax, t,
                     cmap='Blues', norm=LogNorm(1e1, 1e4), alpha=0.75)

    # surface topography
    cs = iplt.contour(nc, 'usurf', ax, t, levels=range(1000, 6000, 1000),
                      cmap=None, colors='k', linewidths=0.1)

    # ice margin
    cs = iplt.icemargin(nc, ax, t, linewidths=0.5)

    # annotate time
    ax.text(0.9, 0.95, '%s ka' % tka, ha='right', va='top',
            bbox=dict(ec='k', fc='w', alpha=1.0),
            transform=ax.transAxes)

    # add triangle
    xy1 = figinvtrans.transform(blendtrans.transform([tkalist[i], 1.0]))
    xy2 = figinvtrans.transform(ax.transAxes.transform([0.0, 0.0]))
    xy3 = figinvtrans.transform(ax.transAxes.transform([1.0, 0.0]))
    tri = Polygon([xy1, xy2, xy3], closed=True, color='0.9', lw=0.1,
                  zorder=-9, transform=fig.transFigure)
    fig.patches.append(tri)

# close extra file
nc.close()

# add colorbar
cax = ax = plt.subplot(gs[0, -1])
cb = fig.colorbar(im, cax, ticks=[1e1, 1e4])
cb.set_label('surf. velocity (m/a)', labelpad=-5)

# add subfigure labels
fig.text(5/figw, 43.75/figh, '(a)', fontweight='bold')
fig.text(5/figw, 31.75/figh, '(b)', fontweight='bold')

# save
print 'saving...'
fig.savefig('plot-snapshots')
