#!/usr/bin/env python2
# coding: utf-8

import numpy as np
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
# redcm = LinearSegmentedColormap.from_list('reds', [darkred, 'w'])
labels = {'grip':    'GRIP',       'ngrip': 'NGRIP',
          'epica':   'EPICA',     'vostok': 'Vostok',
          'odp1012': 'ODP 1012', 'odp1020': 'ODP 1020'}
colors = {'grip':    'b',   'ngrip': 'c',
          'epica':   'r',  'vostok': 'm',
          'odp1012': 'g', 'odp1020': 'y'}
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


def remove_ticks(grid):
    for ax in grid:
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
