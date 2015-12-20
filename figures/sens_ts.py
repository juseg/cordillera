#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt


def fill_between_safe(x, y1, y2, ax=None, **kwargs):
    """Fill between even if y1 and y2 have different lenght."""

    # truncate two arrays to smaller lenght
    minlen = min(len(y1), len(y2))
    y1 = y1[:minlen]
    y2 = y2[:minlen]

    # fill between
    ax = ax or iplt.gca()
    return ax.fill_between(x, y1, y2, **kwargs)


# parameters
res = '10km'
rec = 'grip'
dt = 6.2

# initialize time-series figure
figw, figh = 120.0, 80.01
fig, grid = iplt.subplots_mm(nrows=2, ncols=1, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=10.0, right=2.5, bottom=10.0, top=2.5,
                             wspace=2.5, hspace=2.5)

# initialize lists
time_series = []
ivol_series = []

# loop on records
tabline = ' '*4 + '%-30s '+ '& %6.2f '*3
for i, conf in enumerate(ut.sens.configs):

    # get MIS times
    mis_idces, mis_times = ut.io.get_mis_times(res, rec, dt, config=conf)

    # compute area from extra file
    nc = ut.io.open_extra_file(res, rec, dt, config=conf)
    ex_thk = nc.variables['thk']
    ex_time = nc.variables['time']
    ex_mask = nc.variables['mask']
    ex_idces = [(np.abs(ex_time[:]-t*ut.a2s)).argmin() for t in mis_times]
    mis_iareas = ((ex_thk[ex_idces] >= ut.thkth)*
                  (ex_mask[ex_idces] == 2)).sum(axis=(1,2))*1e-4
    nc.close()

    # get ice volume from time series
    nc = ut.io.open_ts_file(res, rec, dt, config=conf)
    ts_time = nc.variables['time'][:]*ut.s2ka
    ts_ivol = nc.variables['slvol'][:]
    nc.close()
    mis_ivols = ts_ivol[mis_idces]

    # print info in table style
    print tabline % ( (conf,) + tuple(-mis_times/1e3) )
    print tabline % ( ('',) + tuple(mis_iareas) )
    print tabline % ( ('',) + tuple(mis_ivols) ) + '\\\\'

    # append to lists
    time_series.append(ts_time)
    ivol_series.append(ts_ivol)

# plot reference run on top
for ax in grid:
    ax.plot(-time_series[0], ivol_series[0], color=ut.sens.colors[0],
            alpha=0.75, zorder=3)

# plot sensitivity to rheologic parameters
fill_between_safe(-time_series[1], ivol_series[1], ivol_series[2], ax=grid[0],
                  edgecolor=ut.sens.colors[1], facecolor=ut.sens_colors[2],
                  alpha=0.75)

# plot sensitivity to sliding parameters
fill_between_safe(-time_series[3], ivol_series[3], ivol_series[4], ax=grid[1],
                  edgecolor=ut.sens.colors[3], facecolor=ut.sens_colors[4],
                  alpha=0.75)

# set axes properties
for ax in grid:

    # mark true MIS stages
    # source: http://www.lorraine-lisiecki.com/LR04_MISboundaries.txt
    ax.axvspan(71, 57, fc='0.85', lw=0.25, zorder=0)
    ax.axvspan(29, 14, fc='0.85', lw=0.25, zorder=0)
    ax.text((120+71)/2, 9.0, 'MIS 5', ha='center')
    ax.text((71+57)/2, 0.5, 'MIS 4', ha='center')
    ax.text((57+29)/2, 9.0, 'MIS 3', ha='center')
    ax.text((29+14)/2, 0.5, 'MIS 2', ha='center')
    ax.text((14+0)/2, 9.0, 'MIS 1', ha='center')

    # set axes properties
    ax.set_xlim(120.0, 0.0)
    ax.set_ylim(0.0, 11.0)
    ax.set_ylabel('ice volume (m s.l.e.)')
    ax.yaxis.set_label_coords(-0.05, 0.5)
    ax.grid(axis='y')

# set axes properties and save time series
print 'saving timeseries...'
ax.set_xlabel('model age (ka)')
fig.savefig('sens_ts')
