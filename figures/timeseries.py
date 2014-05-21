#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from paperglobals import *

# simulations used
res = '10km'
records = ['grip', 'ngrip', 'epica', 'vostok', 'odp1012', 'odp1020']
offsets = [5.8, 6.0, 5.6, 5.6, 5.8, 5.8]

# initialize time-series figure
figw, figh = 122.51, 80.01
fig = mplt.figure(2, (figw*in2mm, figh*in2mm))
ax1 = fig.add_axes([10/figw, 45/figh, 110/figw, 32.5/figh])
ax2 = fig.add_axes([10/figw, 10/figh, 110/figw, 32.5/figh])
mis_idces = np.zeros((len(records), 3), dtype=int)
mis_times = np.zeros((len(records), 3), dtype=float)

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
    nc = Dataset(run_path % (res, rec, dt*100) + '-ts.nc')
    ts_time = nc.variables['time'][:]*s2ka
    ts_ivol = nc.variables['ivol'][:]*1e-15
    nc.close()

    # plot time series
    ax1.plot(dt_time, dt_temp, color=colors[rec])
    ax2.plot(ts_time, ts_ivol, color=colors[rec])
    ax2.plot(mis_times[i], ts_ivol[mis_idces[i]], ls=' ', mew=0.2, ms=4,
             color=colors[rec], marker=markers[rec], label=labels[rec])

# plot high resolution simu for comparison
res = '5km'
rec = 'grip'
dt = 5.8
print 'plotting hi-res %s time series...' % rec
nc = Dataset(run_path % (res, rec, dt*100) + '-ts.nc')
ts_time = nc.variables['time'][:]*s2ka
ts_ivol = nc.variables['ivol'][:]*1e-15
nc.close()
ax2.plot(ts_time, ts_ivol, color=colors[rec], dashes=(1, 1))

# mark MIS stages
mistmin = mis_times.min(axis=0)
mistmax = mis_times.max(axis=0)
for i in range(3):
    print 'MIS %i between %.1f and %.1f kyr' % (4-i, -mistmin[i], -mistmax[i])
    ax2.axvspan(mistmin[i], mistmax[i], color='0.75', lw=0.0)

# set axes properties and save time series
print 'saving time series...'
ax1.set_xlim(-120.0, 0.0)
ax1.set_ylim(-10.0, 2.0)
ax1.xaxis.set_ticklabels([])
ax1.set_ylabel('temperature offset (K)')
ax2.set_ylabel(r'ice volume (10$^6$ km$^3$)')
ax1.yaxis.set_label_coords(-0.05, 0.5)
ax2.yaxis.set_label_coords(-0.05, 0.5)
ax2.set_xlabel('model time (kyr)')
ax2.legend(loc='upper left', ncol=2)
fig.savefig('timeseries')
