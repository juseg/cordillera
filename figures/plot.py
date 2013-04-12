#!/usr/bin/env python
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import plot as iplt

### Globals ###

mapsize = (30., 60.)
labels = {
  'cfsr':   'CFSR',
  'cfsrs7': 'smoothed CFSR',
  'erai':   'ERA-Interim',
  'narr':   'NARR',
  'ncar':   'NCEP/NCAR',
  'wc':     'WorldClim',
  'wcnn':   'WorldClim'}

### Base function ###

def _plot_maps(climates, clabel, output, func, cticks=None):
    """Base function to plot maps"""

    # initialize figure
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      sm = func(i, clim)

    # add colorbar
    cb = fig.colorbar(sm, fig.grid.cbar_axes[0], ticks=cticks)
    cb.set_label(clabel)

    # save
    print 'saving ' + output
    fig.savefig(output + '.png')
    fig.savefig(output + '.pdf')

### Results plotting functions ###

def _plot_icemaps(climates, offsets, title, output):
    """Base function to plot icemaps"""

    def func(i, clim):
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      plt.title(title % {'label': labels[clim], 'dt': offsets[i]})
      return iplt.icemap(nc)

    _plot_maps(climates, 'ice surface velocity (m/s)', output, func)

def _plot_extents(climates, title, output):
    """Base functiont to plot ice extents"""

    def func(i, clim):
      icecover = 10
      for dt in range(9,-1,-1):
        nc = Dataset('../data/%s-%02g.nc' % (clim, dt))
        thkmask = nc.variables['thk'][0] > 1
        icecover = np.where(nc.variables['thk'][0] > 1, dt, icecover)
      plt.title(title % {'label': labels[clim]})
      #cs = plt.contour(icecover.T,
        #levels = range(0, 10),
        #colors = 'black',
        #linewidths = 0.2)
      return plt.contourf(icecover.T,
        levels = range(-1, 10),
        cmap   = plt.cm.Blues_r)

    _plot_maps(climates, u'temperature offset (°C)', output, func, range(10))

def best():
    """Plot icemaps for the best runs"""
    _plot_icemaps(
      climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar'],
      offsets  = ['09', '07', '08', '05', '04', '05'],
      title    = '%(label)s - %(dt)s K',
      output   = 'cordillera-climate-best')

def cool(cool):
    """Plot icemaps for given temperature offset"""
    _plot_icemaps(
      climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar'],
      offsets  = [cool]*6,
      title    = '%(label)s',
      output   = 'cordillera-climate-cool' + cool)

def extent():
    """Plot stacked ice extents"""
    _plot_extents(
      climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar'],
      title    = '%(label)s',
      output   = 'cordillera-climate-extent')

### Command-line interface ###

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cool',
      help='plot icemaps for given temperature offset')
    parser.add_argument('--best', action='store_true',
      help='plot icemaps for so-called best runs')
    parser.add_argument('--extent', action='store_true',
      help='plot stacked ice extent from all runs')
    args = parser.parse_args()

    if args.cool is not None: cool(args.cool)
    if args.best is True: best()
    if args.extent is True: extent()


