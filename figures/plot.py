#!/usr/bin/env python
# coding: utf-8

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import plot as iplt

### Globals ###

labels = {
  'cfsr':   'CFSR',
  'cfsrs7': 'smoothed CFSR',
  'erai':   'ERA-Interim',
  'narr':   'NARR',
  'ncar':   'NCEP/NCAR',
  'wc':     'WorldClim',
  'wcnn':   'WorldClim'}

### Results plotting functions ###

def _plot_results(climates, offsets, title, output):
    """Base function to plot results"""

    # initialize figure
    fig = iplt.gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):

      # plot
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      ax = plt.axes(fig.grid[i])
      im = iplt.icemap(nc)
      ax.set_title(title % {'label': labels[clim], 'dt': offsets[i]})

      # colorbar
      cb = fig.colorbar(im, fig.grid.cbar_axes[0])
      cb.set_label('ice surface velocity (m/yr)')

    # save
    fig.savefig(output + '.png')
    fig.savefig(output + '.pdf')

def best():
    """Plot icemaps for the best runs"""
    _plot_results(
      climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar'],
      offsets  = ['09', '07', '08', '05', '04', '05'],
      title    = '%(label)s - %(dt)s K',
      output   = 'cordillera-climate-best')

def cool(cool):
    """Plot icemaps for given temperature offset"""
    _plot_results(
      climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar'],
      offsets  = [cool]*6,
      title    = '%(label)s',
      output   = 'cordillera-climate-cool' + cool)

### Command-line interface ###

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cool',
      help='plot icemaps for given temperature offset')
    parser.add_argument('--best', action='store_true',
      help='plot icemaps for so-called best runs')
    args = parser.parse_args()

    if args.cool is not None: cool(args.cool)
    if args.best is not None: best()


