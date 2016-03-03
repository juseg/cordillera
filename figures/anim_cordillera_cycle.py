#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
import cartopy.feature as cfeature
from matplotlib.animation import FuncAnimation

# parameters
res = '5km'
records = ut.hr.records
offsets = ut.hr.offsets
colors = ut.hr.colors
labels = ut.hr.labels

# cartopy features
rivers = cfeature.NaturalEarthFeature(
    category='physical', name='rivers_lake_centerlines', scale='50m',
    edgecolor='0.25', facecolor='none', lw=0.5)
lakes = cfeature.NaturalEarthFeature(
    category='physical', name='lakes', scale='50m',
    edgecolor='0.25', facecolor='0.85', lw=0.25)
graticules = cfeature.NaturalEarthFeature(
    category='physical', name='graticules_5', scale='10m',
    edgecolor='0.25', facecolor='none', lw=0.1)

# drawing function for animations
def draw(t, grid, datasets, labels, cursor):
    age = -t/1e3
    print 'plotting frame at %.1f ka...' % age

    # clear axes
    for ax in grid:
        ax.cla()

    # loop on datasets
    for i, nc in enumerate(datasets):
        ax = grid[i]
        label = labels[i]

        # plot maps
        nc.imshow('topg', ax=ax, t=t,
                  cmap=ut.topo_cmap, norm=ut.topo_norm, zorder=-1)
        nc.contour('topg', ax=ax, t=t, levels=[0.0], cmap=None,
                   colors='0.25', linewidths=0.25, zorder=0)
        nc.icemargin(ax=ax, t=t, linewidths=0.5)
        nc.contour('usurf', ax=ax, t=t, levels=range(200, 5000, 200),
                   cmap=None, colors='k', linewidths=0.1)
        nc.contour('usurf', ax=ax, t=t, levels=range(1000, 5000, 1000),
                   cmap=None, colors='k', linewidths=0.25)
        im = nc.imshow('velsurf_mag', ax=ax, t=t,
                       cmap=ut.vel_cmap, norm=ut.vel_norm, alpha=0.75)
        ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (label, age))

        # add cartopy vectors
        ax.add_feature(rivers, zorder=0)
        ax.add_feature(lakes, zorder=0)
        ax.add_feature(graticules)

        # update cursor
        cursor.set_data([age, age], [0, 1])

    # return mappable for colorbar
    return im

# initialize figure
figw, figh = 135.0, 155.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh), projection=ut.pl.proj,
                             left=2.5, right=20.0, bottom=42.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 42.5/figh, 5.0/figw, 1-45.0/figh])
tsax = fig.add_axes([10.0/figw, 10.0/figh, 1-12.5/figw, 30.0/figh])

# add signature
fig.text(1-2.5/figw, 2.5/figh, 'J. Seguinot et al. (2016)',
         ha='right', va='bottom')

# plot time series
for i, rec in enumerate(records):
    dt = ut.hr.offsets[i]

    # load output time series
    nc = ut.io.open_ts_file('10km', rec, dt)
    ts_time = nc.variables['time'][:]*ut.s2ka
    ts_ivol = nc.variables['slvol'][:]
    nc.close()

    # plot time series
    tsax.plot(-ts_time, ts_ivol, color=colors[i], label=labels[i])

# set axes properties
tsax.invert_xaxis()
tsax.set_xlabel('model age (ka)')
tsax.set_ylim(0.0, 9.5)
tsax.set_ylabel('ice volume (m s.l.e.)')
tsax.grid(axis='y')
tsax.legend(loc='upper left')

# init moving vertical line
cursor = tsax.axvline(60.0, c='k', lw=0.25)

# load extra datasets
datasets = [ut.io.open_extra_file(res, rec, dt)
            for (rec, dt) in zip(records, offsets)]
times = [nc.variables['time'][:]*ut.s2a for nc in datasets]
time = np.intersect1d(*times)

# draw first frame and colorbar
im = draw(time[0], grid, datasets, labels, cursor)
cb = fig.colorbar(im, cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,a^{-1}$)')

# make animation
anim = FuncAnimation(fig, draw, frames=time,
                     fargs=(grid, datasets, labels, cursor))
anim.save('anim_cordillera_cycle', fps=25)

# close datasets
for nc in datasets:
    nc.close()
