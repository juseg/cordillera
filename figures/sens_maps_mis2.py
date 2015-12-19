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

# plot sensitivity to rheologic parameters
for i, conf in enumerate(ut.sens_configs):

    # get MIS2 time
    t = ut.io.get_mis_times(res, rec, dt, config=conf)[1][2]

    # load extra output
    nc = ut.io.open_extra_file(res, rec, dt, config=conf)

    # plot topo and margin from default run
    if i == 0:
        for ax in grid:
            nc.imshow('topg', ax=ax, t=t,
                      cmap=ut.topo_cmap, norm=ut.topo_norm)
            nc.icemargin(ax=ax, t=t, colors=ut.sens_colors[i], zorder=3)

    # plot ice margin from other runs
    elif i <=3:
        nc.icemargin(ax=grid[0], t=t, colors=ut.sens_colors[i])
    else:
        nc.icemargin(ax=grid[1], t=t, colors=ut.sens_colors[i])

    # close
    nc.close()

# set axes properties and save time series
print 'saving...'
fig.savefig('sens_maps_mis2')
