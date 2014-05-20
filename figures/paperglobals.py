#!/usr/bin/env python2
# coding: utf-8

import numpy as np
import brewer2mpl
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap


# unit conversion
in2mm = 1/25.4
s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)


# file paths
pism_dir = '/home/julien/pism/'
atm_file = pism_dir + 'input/atm/cordillera-narr-%s-bl.nc'  # % res
boot_file = pism_dir + 'input/boot/cordillera-etopo1bed-%s.nc'  # % res
dt_file = pism_dir + 'input/dt/%s-3222-cool580.nc'  # % rec
run_path = pism_dir + 'output/cordillera-narr-%s-bl/' \
                      '%s3222cool580+ccyc+till1545/y0120000'  # % res, rec


# colors
bmap = brewer2mpl.get_map('Paired', 'qualitative', 6)
cols = bmap.mpl_colors
lightblue, darkblue = cols[0:2]
lightgreen, darkgreen = cols[2:4]
lightred, darkred = cols[4:6]


# alternative for controlled brightness
#rbmap = brewer2mpl.get_map('Reds', 'sequential', 9)
#bbmap = brewer2mpl.get_map('Blues', 'sequential', 9)
#gbmap = brewer2mpl.get_map('Greens', 'sequential', 9)
#rcols = rbmap.mpl_colors
#gcols = gbmap.mpl_colors
#bcols = bbmap.mpl_colors
#lightred, darkred = rcols[3], rcols[6]
#lightblue, darkblue = bcols[3], bcols[6]
#lightgreen, darkgreen = gcols[3], gcols[6]


# record properties
labels = {'grip':    'GRIP',       'ngrip': 'NGRIP',
          'epica':   'EPICA',     'vostok': 'Vostok',
          'odp1012': 'ODP 1012', 'odp1020': 'ODP 1020'}
colors = {'grip':    darkblue,    'ngrip': lightblue,
          'epica':   darkred,    'vostok': lightred,
          'odp1012': darkgreen, 'odp1020': lightgreen}
markers = {'grip':    's',   'ngrip': 'D',
           'epica':   'o',  'vostok': 'h',
           'odp1012': 'v', 'odp1020': '^'}


# functions
def annotate(ax, s):
    return ax.text(13/15., 28/30., s,
                   va='top', ha='right',
                   bbox=dict(ec='k', fc='w', alpha=1.0),
                   transform=ax.transAxes)


def bounded_argmin(a, coord, bmin, bmax):
    return np.ma.argmin(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def bounded_argmax(a, coord, bmin, bmax):
    return np.ma.argmax(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def get_mis_times(filename):
    """Return MIS indexes and times computed from output timeseries"""

    # load output time series
    nc = Dataset(filename)
    ts_time = nc.variables['time'][:]*s2ka
    ts_ivol = nc.variables['ivol'][:]*1e-15
    nc.close()

    # locate snapshot times using time series
    mis = np.array([
        bounded_argmax(ts_ivol, ts_time, -80, -40),  # MIS4
        bounded_argmin(ts_ivol, ts_time, -60, -20),  # MIS3
        bounded_argmax(ts_ivol, ts_time, -40, -00)])  # MIS2

    # return indices and time values
    return mis, ts_time[mis]

def remove_ticks(grid):
    for ax in grid:
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
