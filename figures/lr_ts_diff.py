#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

offsets = [6.2, 6.6, 5.9, 6.0, 6.1, 5.9]
versions = ('dev-140915-8ff7cbe', '0.7.2-craypetsc')

# initialize time-series figure
figw, figh = 85.0, 80.01
fig, ax = iplt.subplots_mm(nrows=1, ncols=1, sharex=True,
                                   figsize=(figw, figh),
                                   left=10.0, right=2.5, bottom=10.0, top=2.5,
                                   wspace=2.5, hspace=2.5)
mis_idces = np.zeros((6, 3), dtype=int)
mis_times = np.zeros((6, 3), dtype=float)
mis_ivols = np.zeros((6, 3), dtype=float)
mis_iareas = np.zeros((6, 3), dtype=float)

# loop on records[i]
tabline = ' '*4 + '%-8s '+ '& %6.2f '*3
for i, rec in enumerate(ut.lr.records):
    dt = offsets[i]

    # load output time series
    nc1 = ut.io.open_ts_file('10km', rec, dt, version=versions[0])
    nc2 = ut.io.open_ts_file('10km', rec, dt, version=versions[1])
    ts_time = nc1.variables['time'][:] * ut.s2ka
    ts_ivol = nc1.variables['slvol'][:] - nc2.variables['slvol'][:]
    nc1.close()
    nc2.close()

    # plot time series
    ax.plot(-ts_time, ts_ivol, color=ut.lr.colors[i])
    ax.plot(-mis_times[i]/1e3, ts_ivol[mis_idces[i]], ls=' ',
             color=ut.lr.colors[i], marker=ut.lr.markers[i], label=ut.lr.labels[i])

    # look for a high-resolution run
    try:    
        nc1 = ut.io.open_ts_file('5km', rec, dt, version=versions[0])
        nc2 = ut.io.open_ts_file('5km', rec, dt, version=versions[1])
        ts_time = nc1.variables['time'][:] * ut.s2ka
        ts_ivol = nc1.variables['slvol'][:] - nc2.variables['slvol'][:]
        nc1.close()
        nc2.close()
        ax.plot(-ts_time, ts_ivol, color=ut.lr.colors[i], dashes=(1, 1))
    except (ValueError, RuntimeError):
        pass


# mark true MIS stages
# source: http://www.lorraine-lisiecki.com/LR04_MISboundaries.txt
ax.axvspan(71, 57, fc='0.85', lw=0.25)
ax.axvspan(29, 14, fc='0.85', lw=0.25)
ax.text((120+71)/2, -0.15, 'MIS 5', ha='center')
ax.text((71+57)/2, -0.15, 'MIS 4', ha='center')
ax.text((57+29)/2, -0.15, 'MIS 3', ha='center')
ax.text((29+14)/2, -0.15, 'MIS 2', ha='center')
ax.text((14+0)/2, -0.15, 'MIS 1', ha='center')

# set axes properties and save time series
print 'saving diffseries...'
ax.invert_xaxis()
ax.set_xlim(120.0, 0.0)
ax.set_ylim(-0.2, 0.8)
ax.set_ylabel('ice volume (m s.l.e.)')
ax.yaxis.set_label_coords(-0.05, 0.5)
ax.set_xlabel('model age (ka)')
ax.grid(axis='y', c='0.5', ls='-', lw=0.1)
ax.legend(loc='upper left', ncol=2)
ut.pl.savefig(fig)
