#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# parameters
res = '5km'
records = ut.hr.records
offsets = ut.hr.offsets
colors = ut.hr.colors
labels = ut.hr.labels

# drawing function for animations
def draw(grid, datasets, labels, t, cursor):
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
        ut.pl.draw_ne_vectors(ax)
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

        # update cursor
        cursor.set_data([age, age], [0, 1])

    # return mappable for colorbar
    return im

# initialize figure
figw, figh = 120.0, 140.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh), projection=ut.pl.proj,
                             left=2.5, right=20.0, bottom=42.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 42.5/figh, 5.0/figw, 1-45.0/figh])
tsax = fig.add_axes([10.0/figw, 10.0/figh, 1-12.5/figw, 30.0/figh])

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
im = draw(grid, datasets, labels, time[0], cursor)
cb = fig.colorbar(im, cax, extend='both', format='%i',
                  ticks=np.logspace(1, 3.5, 6))
cb.set_label(r'surface velocity ($m\,a^{-1}$)')

# loop on time
for i, t in enumerate(time):

    # save individual frames
    im = draw(grid, datasets, labels, t, cursor)
    fig.savefig('frames/%04i.png' % i)

# close datasets
for nc in datasets:
    nc.close()
