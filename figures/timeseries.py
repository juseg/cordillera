#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.patches import Rectangle
from paperglobals import *

# initialize time-series figure
figw, figh = 120.0, 80.01
fig = mplt.figure(2, (figw*in2mm, figh*in2mm))
ax1 = fig.add_axes([10/figw, 45/figh, 107.5/figw, 32.5/figh])
ax2 = fig.add_axes([10/figw, 10/figh, 107.5/figw, 32.5/figh])
mis_idces = np.zeros((len(records), 3), dtype=int)
mis_times = np.zeros((len(records), 3), dtype=float)
mis_ivols = np.zeros((len(records), 3), dtype=float)

# loop on records[i]
for i, rec in enumerate(records):
    print 'plotting %s time series...' % rec
    dt = offsets[i]

    # get MIS times
    mis_idces[i], mis_times[i] = get_mis_times(run_path % (res, rec, dt*100) + '-ts.nc')

    # load forcing time series
    nc = Dataset(dt_file % (rec, dt*100))
    dt_time = nc.variables['time'][:]*1e-3
    dt_temp = nc.variables['delta_T'][:]
    nc.close()

    # load output time series
    nc = Dataset(run_path % ('10km', rec, dt*100) + '-ts.nc')
    ts_time = nc.variables['time'][:]*s2ka
    ts_ivol = nc.variables['slvol'][:]
    nc.close()
    mis_ivols[i] = ts_ivol[mis_idces[i]]

    # plot time series
    ax1.plot(dt_time, dt_temp, color=colors[i])
    ax2.plot(ts_time, ts_ivol, color=colors[i])
    ax2.plot(mis_times[i], ts_ivol[mis_idces[i]], ls=' ', mew=0.2, ms=4,
             color=colors[i], marker=markers[i], label=labels[i])

    # look for a high-resolution run
    try:
        nc = Dataset(run_path % ('6km', rec, dt*100) + '-ts.nc')
        ts_time = nc.variables['time'][:]*s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        ax2.plot(ts_time, ts_ivol, color=colors[i], dashes=(1, 1))
    except RuntimeError:
        pass

# mark true MIS stages
# source: http://www.lorraine-lisiecki.com/LR04_MISboundaries.txt
ax2.axvspan(-71, -57, fc='0.95', lw=0.25)
ax2.axvspan(-29, -14, fc='0.95', lw=0.25)
ax2.text((-120-71)/2, 4.5, 'MIS 5', ha='center')
ax2.text((-71-57)/2, 0.5, 'MIS 4', ha='center')
ax2.text((-57-29)/2, 8.0, 'MIS 3', ha='center')
ax2.text((-29-14)/2, 0.5, 'MIS 2', ha='center')
ax2.text((-14-0)/2, 8.0, 'MIS 1', ha='center')

# mark modelled glacial extrema
mistmin = mis_times.min(axis=0)
mistmax = mis_times.max(axis=0)
misvmin = mis_ivols.min(axis=0)
misvmax = mis_ivols.max(axis=0)
print misvmin, misvmax
for i in range(3):
    print 'MIS %i between %.1f and %.1f kyr' % (4-i, -mistmin[i], -mistmax[i])
    ax2.add_patch(Rectangle((mistmin[i], misvmin[i]),
                             mistmax[i] - mistmin[i],
                             misvmax[i] - misvmin[i],
                             fc='none', hatch='//', lw=0.25, alpha=0.75))

# set axes properties and save time series
print 'saving time series...'
ax1.set_xlim(-120.0, 0.0)
ax1.set_ylim(-10.0, 2.0)
ax1.xaxis.set_ticklabels([])
ax1.set_ylabel('temperature offset (K)')
ax2.set_ylabel('ice volume (m s.-l. eq.)')
ax1.yaxis.set_label_coords(-0.05, 0.5)
ax2.yaxis.set_label_coords(-0.05, 0.5)
ax2.set_xlabel('model time (kyr)')
ax2.legend(loc='upper left', ncol=2)
fig.savefig('timeseries')
