#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from matplotlib import pyplot as mplt
from matplotlib.patches import Rectangle
from paperglobals import *

# parametres
res = '20km'
dt = 6.0
periods = 3020 + np.arange(5)*101

# initialize time-series figure
figw, figh = 120.0, 80.0
fig, grid = mplt.subplots(2, figsize=(figw*in2mm, figh*in2mm),
                         sharex=True, sharey=False)
fig.subplots_adjust(left=10.0/figw, bottom=10.0/figh,
                    right=1-2.5/figw, top=1-2.5/figh,
                    hspace=1/((1+figh/2.5)/4-1))
ax1, ax2 = grid
mis_idces = np.zeros((len(records), 3), dtype=int)
mis_times = np.zeros((len(records), 3), dtype=float)
mis_ivols = np.zeros((len(records), 3), dtype=float)
print 'per:    min,   max,   std'

# loop on scaling periods
for i, per in enumerate(periods):
    ax1.cla()
    ax2.cla()

    # loop on records[i]
    for j, rec in enumerate(records):

        # get MIS times
        mis_idces[j], mis_times[j] = get_mis_times(res, rec, dt, per)

        # load forcing time series
        nc = open_dt_file(rec, dt, period=per)
        dt_time = nc.variables['time'][:]*1e-3
        dt_temp = nc.variables['delta_T'][:]
        nc.close()

        # load output time series
        nc = open_ts_file(res, rec, dt, period=per)
        ts_time = nc.variables['time'][:]*s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        mis_ivols[j] = ts_ivol[mis_idces[j]]

        # plot time series
        ax1.plot(dt_time, dt_temp, color=colors[j])
        ax2.plot(ts_time, ts_ivol, color=colors[j])
        ax2.plot(mis_times[j], mis_ivols[j], ls=' ', mew=0.2, ms=4,
                 color=colors[j], marker=markers[j], label=labels[j])


    # mark true MIS stages
    # source: http://www.lorraine-lisiecki.com/LR04_MISboundaries.txt
    ax2.axvspan(-71, -57, fc='0.95', lw=0.25)
    ax2.axvspan(-29, -14, fc='0.95', lw=0.25)
    ax2.text((-120-71)/2, 4.5, 'MIS 5', ha='center')
    ax2.text((-71-57)/2, 0.5, 'MIS 4', ha='center')
    ax2.text((-57-29)/2, 8.0, 'MIS 3', ha='center')
    ax2.text((-29-14)/2, 0.5, 'MIS 2', ha='center')
    ax2.text((-14-0)/2, 8.0, 'MIS 1', ha='center')

    # add rectangle
    mis2tmin = mis_times[:,-1].min()
    mis2tmax = mis_times[:,-1].max()
    mis2vmin = mis_ivols[:,-1].min()
    mis2vmax = mis_ivols[:,-1].max()
    ax2.add_patch(Rectangle((mis2tmin, mis2vmin),
                             mis2tmax - mis2tmin,
                             mis2vmax - mis2vmin,
                             fc='none', hatch='//', lw=0.25, alpha=0.75))

    # print additional info
    mis2vstd = mis_ivols[:,-1].std()
    print '%s: %5.2f, %5.2f, %5.2f' % (per, mis2vmin, mis2vmax, mis2vstd)

    # set axes properties
    ax1.grid(axis='y', c='0.5', ls='-', lw=0.1)
    ax2.grid(axis='y', c='0.5', ls='-', lw=0.1)
    ax1.set_xlim(-120.0, 0.0)
    ax1.set_ylim(-10.0, 2.0)
    ax2.set_ylim(0.0, 12.0)
    ax1.set_ylabel('temperature offset (K)')
    ax2.set_ylabel('ice volume (m s.l.e.)')
    ax2.set_xlabel('model time (kyr)')
    ax2.legend(loc='upper left', ncol=2)

    # save figure
    print 'saving plot...'
    fig.savefig('scaling-%s.png' % per)

