#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.patches import Rectangle

# parametres
res = '20km'
dt = 6.0
periods = 3020 + np.arange(5)*101
version = 'dev-140915-8ff7cbe'

# initialize time-series figure
fig, grid = iplt.subplots_mm(5, 2, sharex=True, figsize=(240.0, 160.0),
                             left=10.0, right=2.5, bottom=10.0, top=2.5,
                             wspace=12.5, hspace=2.5)
mis_idces = np.zeros((len(ut.records), 3), dtype=int)
mis_times = np.zeros((len(ut.records), 3), dtype=float)
mis_ivols = np.zeros((len(ut.records), 3), dtype=float)
print 'per:    min,   max,   std'

# loop on scaling periods
for i, per in enumerate(periods):
    ax1 = grid[i][0]
    ax2 = grid[i][1]

    # loop on records[i]
    for j, rec in enumerate(ut.records):

        # get MIS times
        mis_idces[j], mis_times[j] = ut.io.get_mis_times(res, rec, dt, per,
                                                         version=version)

        # load forcing time series
        nc = ut.io.open_dt_file(rec, dt, period=per)
        dt_time = nc.variables['time'][:]*1e-3
        dt_temp = nc.variables['delta_T'][:]
        nc.close()

        # load output time series
        nc = ut.io.open_ts_file(res, rec, dt, period=per, version=version)
        ts_time = nc.variables['time'][:]*ut.s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        mis_ivols[j] = ts_ivol[mis_idces[j]]

        # plot time series
        ax1.plot(-dt_time, dt_temp, color=ut.colors[j])
        ax2.plot(-ts_time, ts_ivol, color=ut.colors[j])
        ax2.plot(-mis_times[j]/1e3, mis_ivols[j], ls=' ', mew=0.2, ms=4,
                 color=ut.colors[j], marker=ut.markers[j], label=ut.labels[j])

    # mark scaling period
    ps, pe = per/100, per%100
    ax1.axvspan(ps, pe, fc='0.85', lw=0.25)
    ax1.text((ps+pe)/2, 0.5, per, ha='center')

    # mark true MIS stages
    # source: http://www.lorraine-lisiecki.com/LR04_MISboundaries.txt
    ax2.axvspan(71, 57, fc='0.85', lw=0.25)
    ax2.axvspan(29, 14, fc='0.85', lw=0.25)

    # add rectangle
    mis2tmin = mis_times[:,-1].min()
    mis2tmax = mis_times[:,-1].max()
    mis2vmin = mis_ivols[:,-1].min()
    mis2vmax = mis_ivols[:,-1].max()
    ax2.add_patch(Rectangle((-mis2tmin/1e3, mis2vmin),
                             -(mis2tmax-mis2tmin)/1e3,
                             mis2vmax - mis2vmin,
                             fc='none', hatch='//', lw=0.25, alpha=0.75))

    # print additional info
    mis2vstd = mis_ivols[:,-1].std()
    print '%s: %5.2f, %5.2f, %5.2f' % (per, mis2vmin, mis2vmax, mis2vstd)

    # set common axes properties
    ax2.invert_xaxis()
    ax1.set_xlim(120.0, 0.0)
    ax1.set_ylim(-10.0, 2.0)
    ax2.set_ylim(0.0, 12.0)
    ax1.set_ylabel('temperature offset (K)')
    ax2.set_ylabel('ice volume (m s.l.e.)')
    ax1.yaxis.set_label_coords(-0.05, 0.5)
    ax2.yaxis.set_label_coords(-0.05, 0.5)
    ax1.grid(axis='y')
    ax2.grid(axis='y')

# label MIS stages
ax2.text((120+71)/2, 4.5, 'MIS 5', ha='center')
ax2.text((71+57)/2, 0.5, 'MIS 4', ha='center')
ax2.text((57+29)/2, 8.0, 'MIS 3', ha='center')
ax2.text((29+14)/2, 0.5, 'MIS 2', ha='center')
ax2.text((14+0)/2, 8.0, 'MIS 1', ha='center')

# set unique axes properties
ax1.set_xlabel('model age (ka)')
ax2.set_xlabel('model age (ka)')
ax2.legend(loc='upper left', ncol=2)

# save figure
print 'saving plot...'
fig.savefig('lr_ts_scaling')

