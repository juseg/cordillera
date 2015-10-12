#!/usr/bin/env python2
# coding: utf-8

from paperglobals import *
from matplotlib.patches import Rectangle

# initialize time-series figure
figw, figh = 120.0, 80.01
fig, (ax1, ax2) = iplt.subplots_mm(nrows=2, ncols=1, sharex=True,
                                   figsize=(figw, figh),
                                   left=10.0, right=2.5, bottom=10.0, top=2.5,
                                   wspace=2.5, hspace=2.5)
mis_idces = np.zeros((len(records), 3), dtype=int)
mis_times = np.zeros((len(records), 3), dtype=float)
mis_ivols = np.zeros((len(records), 3), dtype=float)
mis_iareas = np.zeros((len(records), 3), dtype=float)

# loop on records[i]
tabline = ' '*4 + '%-8s '+ '& %6.2f '*3
for i, rec in enumerate(records):
    dt = offsets[i]

    # get MIS times
    mis_idces[i], mis_times[i] = get_mis_times(res, rec, dt)

    # compute area from extra file
    nc = open_extra_file(res, rec, dt)
    ex_thk = nc.variables['thk']
    ex_time = nc.variables['time']
    ex_idces = [(np.abs(ex_time[:]-t*a2s)).argmin() for t in mis_times[i]]
    mis_iareas[i] = (ex_thk[ex_idces] > thkth).sum(axis=(1,2))*1e-4
    nc.close()

    # load forcing time series
    nc = open_dt_file(rec, dt)
    dt_time = nc.variables['time'][:]*1e-3
    dt_temp = nc.variables['delta_T'][:]
    nc.close()

    # load output time series
    nc = open_ts_file('10km', rec, dt)
    ts_time = nc.variables['time'][:]*s2ka
    ts_ivol = nc.variables['slvol'][:]
    nc.close()
    mis_ivols[i] = ts_ivol[mis_idces[i]]

    # print info in table style
    tabline = ' '*4 + '%-8s '+ '& %6.2f '*3
    print tabline % ( (labels[i],) + tuple(-mis_times[i]/1e3) )
    print tabline % ( ('',) + tuple(mis_iareas[i]) )
    print tabline % ( ('',) + tuple(mis_ivols[i]) ) + '\\\\'

    # plot time series
    ax1.plot(-dt_time, dt_temp, color=colors[i])
    ax2.plot(-ts_time, ts_ivol, color=colors[i])
    ax2.plot(-mis_times[i], ts_ivol[mis_idces[i]], ls=' ', mew=0.2, ms=4,
             color=colors[i], marker=markers[i], label=labels[i])

    # look for a high-resolution run
    try:
        nc = open_ts_file('5km', rec, dt)
        ts_time = nc.variables['time'][:]*s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        ax2.plot(-ts_time, ts_ivol, color=colors[i], dashes=(1, 1))
    except RuntimeError:
        pass


# mark true MIS stages
# source: http://www.lorraine-lisiecki.com/LR04_MISboundaries.txt
ax2.axvspan(71, 57, fc='0.85', lw=0.25)
ax2.axvspan(29, 14, fc='0.85', lw=0.25)
ax2.text((120+71)/2, 4.5, 'MIS 5', ha='center')
ax2.text((71+57)/2, 0.5, 'MIS 4', ha='center')
ax2.text((57+29)/2, 8.5, 'MIS 3', ha='center')
ax2.text((29+14)/2, 0.5, 'MIS 2', ha='center')
ax2.text((14+0)/2, 8.5, 'MIS 1', ha='center')

# mark modelled glacial extrema
mistmin = mis_times.min(axis=0)
mistmax = mis_times.max(axis=0)
misvmin = mis_ivols.min(axis=0)
misvmax = mis_ivols.max(axis=0)
misamin = mis_iareas.min(axis=0)
misamax = mis_iareas.max(axis=0)
for i in range(3):
    ax2.add_patch(Rectangle((-mistmin[i]/1e3, misvmin[i]),
                             -(mistmax[i]-mistmin[i])/1e3,
                             misvmax[i] - misvmin[i],
                             fc='none', hatch='//', lw=0.25, alpha=0.75))

# print info in table style
print tabline % ( ('Minimum',) + tuple(-mistmin/1e3) )
print tabline % ( ('',) + tuple(misamin) )
print tabline % ( ('',) + tuple(misvmin) ) + '\\\\'
print tabline % ( ('Maximum',) + tuple(-mistmax/1e3) )
print tabline % ( ('',) + tuple(misamax) )
print tabline % ( ('',) + tuple(misvmax) ) + '\\\\'

# set axes properties and save time series
print 'saving timeseries...'
ax2.invert_xaxis()
ax1.set_xlim(120.0, 0.0)
ax1.set_ylim(-10.0, 2.0)
ax2.set_ylim(0.0, 9.5)
ax1.set_ylabel('temperature offset (K)')
ax2.set_ylabel('ice volume (m s.l.e.)')
ax1.yaxis.set_label_coords(-0.05, 0.5)
ax2.yaxis.set_label_coords(-0.05, 0.5)
ax2.set_xlabel('model age (ka)')
ax1.grid(axis='y', c='0.5', ls='-', lw=0.1)
ax2.grid(axis='y', c='0.5', ls='-', lw=0.1)
ax2.legend(loc='upper left', ncol=2)
fig.savefig('timeseries')
