#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# parameters
res = '10km'
rec = 'grip'

# initialize figure
fig, grid = iplt.subplots_mm(nrows=3, ncols=1, sharex=True, sharey=True,
                             figsize=(120.0, 100.0),
                             left=10.0, right=2.5, bottom=10.0, top=2.5,
                             wspace=2.5, hspace=2.5)

# build velocity distributions
vdistlists=[[], [], []]
for i, conf in enumerate(ut.sens.configs):
    dt = ut.sens.offsets[i]

    # get MIS times
    mis_idces, mis_times = ut.io.get_mis_times(res, rec, dt, config=conf)

    # open extra file
    nc = ut.io.open_extra_file(res, rec, dt, config=conf)
    time = nc.variables['time']
    thk = nc.variables['thk']
    v = nc.variables['velsurf_mag']

    # compute velocity dist for each mis
    vdist = []
    for j, t in enumerate(mis_times):
        idx = (np.abs(time[:]-t*ut.a2s)).argmin()
        mask = (thk[idx] >= ut.thkth)
        vdist = v[idx][mask]
        vdist = np.log10(vdist)
        vdistlists[j].append(vdist)
    nc.close()

# plot
for i, ax in enumerate(grid):
    violins = ax.violinplot(vdistlists[i])
    for p, c in zip(violins['bodies'], ut.sens.colors):
        p.set_color(c)
    violins['cbars'].set_color('0.5')
    violins['cmins'].set_color('0.5')
    violins['cmaxes'].set_color('0.5')
    ax.text(0.5, 4.5, 'MIS %d' % (4-i))
    ax.grid(axis='y')

# set axes properties
ax.set_ylim(-0.5, 5.5)
ax.set_xticks(range(1,6))
ax.set_xticklabels(ut.sens.labels)
grid[1].set_ylabel(r'log of surface velocity ($m\,a^{-1}$)')

# save
ut.pl.savefig(fig)
