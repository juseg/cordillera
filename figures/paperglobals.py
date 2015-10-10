#!/usr/bin/env python2
# coding: utf-8

# FIXME: make iceplotlib a package
import sys
sys.path.append('iceplotlib')

import os
import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from matplotlib.transforms import ScaledTranslation
from iceplotlib.cm import velocity
from iceplotlib import plot as iplt


# unit conversion
in2mm = 1/25.4
pt2mm = 72*in2mm
s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)

# file paths
pism_dir = os.environ['HOME'] + '/pism/'

# default params
res = '10km'
dt = 5.8
rec = 'grip'

# colors
topo_cmap = 'Greys'
topo_norm = Normalize(-3000, 6000)
vel_cmap = 'RdBu_r'
vel_norm = LogNorm(1e1, 1e3)

# record properties
records = ['grip', 'ngrip', 'epica', 'vostok', 'odp1012', 'odp1020']
labels = ['GRIP', 'NGRIP', 'EPICA', 'Vostok', 'ODP 1012', 'ODP 1020']
colors = ['#1F78B4', '#A6CEE3', '#E31A1C', '#FB9A99', '#33A02C', '#B2DF8A']
markers = ['s', 'D', 'o', 'h', 'v', '^']
offsets = [6.1, 6.5, 5.9, 5.9, 6.1, 6.0]

# default thickness threshold
thkth = 1.0


# file open functions
def open_atm_file(res):
    return iplt.load(pism_dir + 'input/atm/cordillera-narr-%s.cr.nc' % res)


def open_boot_file(res):
    return iplt.load(pism_dir + 'input/boot/cordillera-etopo1bed-%s.cr.nc'
                     % res)


def open_dt_file(rec, dt, period='3222'):
    return iplt.load(pism_dir + 'input/dt/%s-%s-cool%i.nc'
                     % (rec, period, round(100*dt)))


def open_sd_file(res):
    return iplt.load(pism_dir + 'input/sd/cordillera-narr-%s.cr.nc' % res)


def open_ts_file(res, rec, dt, period='3222'):
    return iplt.load(pism_dir + 'output/dev-140915-8ff7cbe/cordillera-narr-%s/'
                     '%s%scool%i+ccyc4+till1545/y0??0000-ts.nc'
                     % (res, rec, period, round(100*dt)))


def open_extra_file(res, rec, dt, period='3222'):
    return iplt.load(pism_dir + 'output/dev-140915-8ff7cbe/cordillera-narr-%s/'
                     '%s%scool%i+ccyc4+till1545/y0??0000-extra.nc'
                     % (res, rec, period, round(100*dt)))


# analysis functions
def bounded_argmin(a, coord, bmin, bmax):
    return np.ma.argmin(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def bounded_argmax(a, coord, bmin, bmax):
    return np.ma.argmax(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def get_mis_times(res, rec, dt, period='3222'):
    """Return MIS indexes and times computed from output timeseries"""

    # load output time series
    nc = open_ts_file(res, rec, dt, period=period)
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


# plotting functions
def add_corner_tag(ax, s, ha='right', va='top'):
    fig = ax.get_figure()
    x = (ha == 'right')  # 0 for left edge, 1 for right edge
    y = (va == 'top')  # 0 for bottom edge, 1 for top edge
    xoffset = (1 - 2*x)*2.5*in2mm
    yoffset = (1 - 2*y)*2.5*in2mm
    offset = ScaledTranslation(xoffset, yoffset, fig.dpi_scale_trans)
    return ax.text(x, y, s, ha=ha, va=va,
                   bbox=dict(ec='k', fc='w', pad=2.5*pt2mm),
                   transform=ax.transAxes + offset)


def add_pointer_tag(ax, s, xy, xytext):
    return ax.annotate(s, xy=xy, xytext=xytext, ha='center', va='center',
                       xycoords='data', textcoords='data',
                       bbox=dict(ec='k', fc='w', boxstyle='square'),
                       arrowprops=dict(arrowstyle="->"))


def draw_boot_topo(grid, res):
    nc = open_boot_file(res)
    for ax in grid.flat:
        im = ax.imshow(nc, 'topg',
                       cmap=topo_cmap, norm=topo_norm)
    nc.close()
    return im


def draw_coastline(grid, res):
    nc = open_boot_file(res)
    for ax in grid.flat:
        cs = ax.contour(nc, 'topg', levels=[0.0],
                        cmap=None, colors='k', linewidths=0.5)
    nc.close()
    return cs
