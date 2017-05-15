#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# parameters
res = '10km'
rec = 'grip'

# initialize figure
figw, figh = 85.0, 110.0
fig, grid = iplt.subplots_mm(nrows=2, ncols=3, sharex=True, sharey=True,
                             figsize=(figw, figh), projection=ut.pl.proj,
                             left=2.5, right=2.5, bottom=2.5, top=5.0,
                             wspace=2.5, hspace=2.5)

# compute ice masks
icemasks=[[], [], []]
for i, conf in enumerate(ut.sens.configs):
    dt = ut.sens.offsets[i]

    # get MIS times
    mis_idces, mis_times = ut.io.get_mis_times(res, rec, dt, config=conf)

    # load extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-10km/'
                    'grip3222cool%03d+%s/y???????-extra.nc'
                    % (round(100*dt), conf))

    # compute ice mask for each MIS
    for j, t in enumerate(mis_times):
        mask = nc._extract_mask(t=t)
        icemasks[j].append(mask)

        # plot topo and margin from default run
        if i == 0:
            x, y, thk = nc._extract_xyz('thk', t=t)
            for ax in grid[:, j]:
                nc.imshow('topg', ax=ax, t=t,
                          cmap=ut.topo_cmap, norm=ut.topo_norm, zorder=-1)
                ut.pl.draw_ne_vectors(ax)
                nc.contour('topg', ax=ax, t=t, levels=[0.0], cmap=None,
                           colors='0.25', linewidths=0.25, zorder=0)
                nc.icemargin(ax=ax, t=t, colors=ut.sens.colors[i], zorder=3)

    # close
    nc.close()

# for each MIS stage
for j in range(3):

    # plot sensitivity to rheologic parameters
    mask = icemasks[j][2]-icemasks[j][1]
    grid[0][j].contourf(x, y, mask, levels=[0.5, 1.5], colors=ut.sens.colors[1],
                        alpha=0.75)
    grid[0][j].contour(x, y, mask, levels=[0.5], colors=ut.sens.colors[2])

    # plot sensitivity to sliding parameters
    mask = icemasks[j][4]-icemasks[j][3]
    grid[1][j].contourf(x, y, mask, levels=[0.5, 1.5], colors=ut.sens.colors[3],
                        alpha=0.75)
    grid[1][j].contour(x, y, mask, levels=[0.5], colors=ut.sens.colors[4])

# add labels
for j in range(3):
    ax = grid[0][j]
    ax.text(0.5, 1.04, 'MIS %i' % (4-j), ha='center', transform=ax.transAxes)

# save
ut.pl.savefig(fig)
