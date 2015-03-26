#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import os
import numpy as np
import brewer2mpl
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize
from matplotlib.transforms import ScaledTranslation
from iceplot.cm import velocity
from iceplot import plot as iplt


# unit conversion
in2mm = 1/25.4
pt2mm = 72*in2mm
s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)


# file paths
pism_dir = os.environ['HOME'] + '/pism/'
atm_file = pism_dir + 'input/atm/cordillera-narr-%s-bl.nc'  # % res
boot_file = pism_dir + 'input/boot/cordillera-etopo1bed-%s.nc'  # % res
dt_file = pism_dir + 'input/dt/%s-3222-cool%i.nc'  # % rec, 10*dt
run_path = (pism_dir + 'output/dev-140915-8ff7cbe/cordillera-narr-%s-bl/'
            '%s3222cool%i+ccyc4+till1545/y0120000')  # % res, rec, 10*dt

# default params
res = '10km'
dt = 5.8
rec = 'grip'

# colors
palette = brewer2mpl.get_map('Paired', 'qualitative', 6).mpl_colors
lightblue, darkblue = palette[0:2]
lightgreen, darkgreen = palette[2:4]
lightred, darkred = palette[4:6]
topo_cmap = 'Greys'
topo_norm = Normalize(-3000, 6000)
vel_cmap = 'RdBu_r'
vel_norm = LogNorm(1e1, 1e3)

# alternative velocity colormap
#vel_cols = ['w', darkblue, darkgreen, '#ffff99', darkred, 'k']
#vel_cmap = LinearSegmentedColormap.from_list('vel', vel_cols)

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
records = ['grip', 'ngrip', 'epica', 'vostok', 'odp1012', 'odp1020']
labels = ['GRIP', 'NGRIP', 'EPICA', 'Vostok', 'ODP 1012', 'ODP 1020']
colors = [darkblue, lightblue, darkred, lightred, darkgreen, lightgreen]
markers = ['s', 'D', 'o', 'h', 'v', '^']
offsets = [6.0, 6.4, 5.8, 5.9, 6.0, 5.7]

# default thickness threshold
thkth = 1.0


# analysis functions
def ncopen(filepath):
    from netCDF4 import Dataset
    nc = Dataset(filepath)
    return nc


def bounded_argmin(a, coord, bmin, bmax):
    return np.ma.argmin(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def bounded_argmax(a, coord, bmin, bmax):
    return np.ma.argmax(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def get_mis_times(filename):
    """Return MIS indexes and times computed from output timeseries"""

    # load output time series
    nc = ncopen(filename)
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
def annotate(ax, s, bottom=False):
    fig = ax.get_figure()
    xoffset = -2.5*in2mm
    yoffset = (2*bottom-1)*2.5*in2mm  # pos. if bottom else neg.
    offset = ScaledTranslation(xoffset, yoffset, fig.dpi_scale_trans)
    return ax.text(1, 1-bottom, s,
                   ha='right', va=('bottom' if bottom else 'top'),
                   bbox=dict(ec='k', fc='w', alpha=1.0, pad=2.5*pt2mm),
                   transform=ax.transAxes + offset)


def draw_boot_topo(grid, res):
    from matplotlib.pyplot import sca
    nc = ncopen(boot_file % res)
    for ax in grid:
        sca(ax)
        im = iplt.imshow(nc, 'topg',
                         cmap=topo_cmap, norm=topo_norm)
    nc.close()
    return im


def draw_coastline(grid, res):
    from matplotlib.pyplot import sca
    nc = ncopen(boot_file % res)
    for ax in grid:
        sca(ax)
        cs = iplt.contour(nc, 'topg', levels=[0.0],
                          cmap=None, colors='k', linewidths=0.5)
    nc.close()
    return cs


def remove_ticks(grid):
    for ax in grid:
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
