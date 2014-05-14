#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from iceplot import plot as iplt

# file paths
dt_file = '/home/julien/pism/input/dt/%s-cool600.nc'  # % rec
run_path = '/home/julien/pism/output/cordillera-narr-10km-bl/' \
           '%scool600+pddc+pddref00+mt8+lc+nofloat+part' \
           '+gflx70+ssa+pp+nfrac02+till1545/y0120000'  # % rec

# unit conversion
mm = 1/25.4
ka = 365.0 * 24 * 60 * 60 * 1000

# records used
records = ['grip', 'epica', 'vostok', 'odp1012', 'odp1020']
labels = ['GRIP', 'EPICA', 'Vostok', 'ODP 1012', 'ODP 1020']
colors = ['b', 'g', 'r', 'c', 'm', 'y']

# initialize time-series figure
figw, figh = 122.51, 80.01
ts_fig = mplt.figure(2, (figw*mm, figh*mm))
ts_ax1 = ts_fig.add_axes([10/figw, 45/figh, 110/figw, 32.5/figh])
ts_ax2 = ts_fig.add_axes([10/figw, 10/figh, 110/figw, 32.5/figh])

# initialize snapshots figure
rect = [2.5/figw, 2.5/figh, 110/figw, 95/figh]
sn_fig = iplt.gridfigure((17.5, 35.0), (3, len(records)), axes_pad=2.5*mm,
                         cbar_mode='none', cbar_location='bottom',
                         cbar_pad=2.5*mm, cbar_size=5*mm)
sn_grid = sn_fig.grid

# loop on records
for i, rec in enumerate(records):

    # load forcing time series
    print 'reading %s temperature offset tme series...' % rec
    nc = Dataset(dt_file % rec)
    dt_time = nc.variables['time'][:]
    dt_temp = nc.variables['delta_T'][:]
    nc.close()

    # load output time series
    print 'reading %s ice volume time series...' % rec
    nc = Dataset(run_path % rec + '-ts.nc')
    ts_time = nc.variables['time'][:]
    ts_ivol = nc.variables['ivol'][:]*1e-15
    nc.close()

    # locate snapshot times using time series
    snapindexes = [
        #np.ma.argmin(np.ma.array(ts_ivol, mask=(ts_time<-115*ka)+(-110*ka<ts_time))),  # Eem
        #np.ma.argmax(np.ma.array(ts_ivol, mask=(ts_time<-100*ka)+(-80*ka<ts_time))),  # 80ka
        np.ma.argmax(np.ma.array(ts_ivol, mask=(ts_time<-80*ka)+(-40*ka<ts_time))),  # MIS4
        np.ma.argmin(np.ma.array(ts_ivol, mask=(ts_time<-60*ka)+(-20*ka<ts_time))),  # MIS3
        np.ma.argmax(np.ma.array(ts_ivol, mask=(ts_time<-40*ka)+(-00*ka<ts_time))),  # MIS2
        #np.ma.argmax(np.ma.array(ts_ivol, mask=(ts_time<-13*ka)+(-11*ka<ts_time))),  # YD
        #np.ma.argmin(np.ma.array(ts_ivol, mask=(ts_time<-20*ka)+(-00*ka<ts_time))),  # Holo
    ]
    snaptimes = ts_time[snapindexes]

    # plot time series
    print 'plotting %s time series...' % rec
    ts_ax1.plot(dt_time/1e3, dt_temp, color=colors[i], label=rec)
    ts_ax2.plot(ts_time/ka, ts_ivol, color=colors[i], label=rec)
    ts_ax2.plot(snaptimes/ka, ts_ivol[snapindexes], color=colors[i], ls=' ',
                marker='o', mew=0.0)

    # load extra output
    print 'reading %s extra output...' % rec
    nc = Dataset(run_path % rec + '-extra.nc')
    time = nc.variables['time'][:]
    thk = nc.variables['thk']

    # round snapshot times to nearest slice
    print 'rounding %s snapshot times...' % rec
    snapindexes = [(np.abs(time[:]-t)).argmin() for t in snaptimes]
    snaptimes = time[snapindexes]

    # plot maps
    for j, t in enumerate(snapindexes):
        print 'plotting %s at %s...' % (rec, snaptimes[j]/ka)
        ax = sn_grid[i+j*len(records)]
        mplt.sca(ax)
        iplt.bedtopoimage(nc, t)
        iplt.icemargincontour(nc, t)
        iplt.surftopocontour(nc, t, levels=range(250, 5000, 250),
                             linewidths=0.2)
        iplt.surftopocontour(nc, t, levels=range(1000, 5000, 1000))
        im = iplt.surfvelimage(nc, t, alpha=0.5)
        mplt.text(13/15., 28/30., '%s kyr' % (snaptimes[j]/ka),
                 va='top', ha='right',
                 bbox=dict(ec='none', fc='w', alpha=0.75),
                 transform=ax.transAxes)

    # close extra file
    nc.close()

# set axes properties and save time series
print 'saving time series...'
ts_ax1.set_xlim(-120.0, 0.0)
ts_ax1.set_ylim(-10.0, 2.0)
ts_ax1.xaxis.set_ticklabels([])
ts_ax1.set_ylabel('temperature offset (K)')
ts_ax2.set_ylabel(r'ice volume (10$^6$ km$^3$)')
ts_ax1.yaxis.set_label_coords(-5/200., 0.5)
ts_ax2.yaxis.set_label_coords(-5/200., 0.5)
ts_ax2.set_xlabel('model time (kyr)')
ts_ax2.legend(loc='upper left', ncol=2)
ts_fig.savefig('cordillera-cycle-multirec-timeseries.png')

# add colorbar and save snapshots
print 'saving snapshots...'
#cb = sn_fig.colorbar(im, ax.cax, orientation='horizontal')
#cb.set_label(r'ice surface velocity ($m\,a^{-1}$)')
sn_fig.savefig('cordillera-cycle-multirec-snapshots.png')
