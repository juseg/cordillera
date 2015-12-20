#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# parameters
res = '10km'
rec = 'grip'
dt = 6.2

# initialize time-series figure
figw, figh = 120.0, 100.0
fig, grid = iplt.subplots_mm(nrows=1, ncols=2, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)

icemasks = []

# plot sensitivity to rheologic parameters
for i, conf in enumerate(ut.sens_configs):

    # get MIS2 time
    t = ut.io.get_mis_times(res, rec, dt, config=conf)[1][2]

    # load extra output
    nc = ut.io.open_extra_file(res, rec, dt, config=conf)
    x, y, thk = nc._extract_xyz('thk', t=t)
    mask = nc._extract_mask(t=t)

    # plot topo and margin from default run
    if i == 0:
        for ax in grid:
            nc.imshow('topg', ax=ax, t=t,
                      cmap=ut.topo_cmap, norm=ut.topo_norm)
            nc.icemargin(ax=ax, t=t, colors=ut.sens_colors[i], zorder=3)

    # close
    nc.close()

    # append
    icemasks.append(mask)

# plot sensitivity to rheologic parameters
mask = icemasks[2]-icemasks[1]
grid[0].contourf(x, y, mask, levels=[0.5, 1.5], colors=ut.sens_colors[2],
                 alpha=0.75)
grid[0].contour(x, y, mask, levels=[0.5], colors=ut.sens_colors[1])

# plot sensitivity to sliding parameters
mask = icemasks[4]-icemasks[3]
grid[1].contourf(x, y, mask, levels=[0.5, 1.5], colors=ut.sens_colors[4],
                 alpha=0.75)
grid[1].contour(x, y, mask, levels=[0.5], colors=ut.sens_colors[3])

# set axes properties and save time series
print 'saving...'
fig.savefig('sens_maps_mis2')
