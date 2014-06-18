#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from matplotlib.patches import Rectangle
from paperglobals import *

# parameters
records = ['grip', 'epica']
offsets = [5.8, 5.6]
colors = [darkblue, darkred]

# initialize time-series figure
figw, figh = 85.01, 80.01
fig = mplt.figure(2, (figw*in2mm, figh*in2mm))
ax1 = fig.add_axes([10/figw, 45/figh, 72.5/figw, 32.5/figh])
ax2 = fig.add_axes([10/figw, 10/figh, 72.5/figw, 32.5/figh])

# loop on records[i]
for i, rec in enumerate(records):
    print 'plotting %s time series...' % rec
    dt = offsets[i]

    # plot forcing time series
    nc = Dataset(dt_file % (rec, dt*100))
    dt_time = nc.variables['time'][:]*1e-3
    dt_temp = nc.variables['delta_T'][:]
    nc.close()
    ax1.plot(dt_time, dt_temp, color=colors[i], label=labels[i])

    # plot output time series
    for res in ('10km', '6km'):
        nc = Dataset(run_path % (res, rec, dt*100) + '-ts.nc')
        ts_time = nc.variables['time'][:]*s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        ax2.plot(ts_time, ts_ivol, color=colors[i],
                 dashes=((None, None) if res == '10km' else (1, 1)),
                 label='%s %s' % (rec.upper(), res))

# set axes properties and save time series
print 'saving...'
ax1.set_xlim(-25.0, -5.0)
ax2.set_xlim(-25.0, -5.0)
ax1.set_ylim(-10.0, 2.0)
ax1.set_xticklabels([])
ax1.set_ylabel('temperature offset (K)')
ax2.set_ylabel('ice volume (m s.-l. eq.)')
ax1.yaxis.set_label_coords(-0.075, 0.5)
ax2.yaxis.set_label_coords(-0.075, 0.5)
ax2.set_xlabel('model time (kyr)')
ax2.legend(loc='upper right')
ax1.grid(axis='y', c='0.5', ls='-', lw=0.1)
ax2.grid(axis='y', c='0.5', ls='-', lw=0.1)
fig.savefig('deglacseries')
