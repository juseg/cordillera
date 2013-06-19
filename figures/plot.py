#!/usr/bin/env python
# coding: utf-8

import numpy as np
import shapefile
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap
from iceplot import plot as iplt
from iceplot import cm as icm

from matplotlib import rc
rc('text', usetex=True)
rc('text.latex', unicode=True)
rc('mathtext', default='regular')

### Globals ###

pismdir = '/home/julien/work/code/pism'
shpfile = '/home/julien/work/data/dyke-deglaciation/16.8-ka.shp'
mapsize = (30., 60.)
labels = {
  'etopo':  'ETOPO1',
  'cfsr':   'CFSR',
  'cfsrs7': 'smoothed CFSR',
  'erai':   'ERA-Interim',
  'narr':   'NARR',
  'ncar':   'NCEP/NCAR',
  'wc':     'WorldClim',
  'wcnn':   'WorldClim'}

### Base function ###

def _plot_maps(climates, clabel, output, func, ci=-1, cticks=None, margin=False):
    """Base function to plot maps"""

    # initialize figure
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    sm = []
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      sm.append(func(i, clim))

    # add LGM ice margin
    if margin is True:
      nc = Dataset('../data/%s-00.nc' % (climates[0]))
      m = Basemap(projection='lcc',
        lat_1=49, lat_2=77, lat_0=49, lon_0=-95,
        llcrnrlat=nc.variables['lat'][0,0],
        urcrnrlat=nc.variables['lat'][-1,-1],
        llcrnrlon=nc.variables['lon'][0,0],
        urcrnrlon=nc.variables['lon'][-1,-1])
      sf = shapefile.Reader(shpfile)
      for record, shape in zip(sf.records(),sf.shapes()):
        lons,lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T/10000
        #lines.set_facecolors('blue')
        #lines.set_edgecolors('k')
        #lines.set_linewidth(0.1)
      for ax in fig.grid:
        lines = LineCollection([data,], antialiaseds=(1,))
        ax.add_collection(lines)

    # add colorbar
    cb = fig.colorbar(sm[ci], fig.grid.cbar_axes[0], ticks=cticks)
    cb.set_label(clabel)

    # save
    print 'saving ' + output
    fig.savefig(output + '.png')
    fig.savefig(output + '.pdf')

### Climate plotting functions ###

def temp():
    """Plot air temperature maps"""

    seasons  = ['jja']*3 + ['djf'] + ['jja']*2

    def func(i, clim):
      nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
      plt.title('%s %s' % (labels[clim], seasons[i].upper()))
      var = nc.variables['air_temp']
      if seasons[i] == 'jja': data = (var[5]  + var[6] + var[7]).T/3
      if seasons[i] == 'djf': data = (var[11] + var[0] + var[1]).T/3
      data = np.ma.masked_equal(data, 0)
      return plt.imshow(data - 273.15,
        cmap = plt.cm.Spectral_r,
        norm = mcolors.Normalize(-30, 30))

    _plot_maps(
      climates = ['wc', 'erai', 'narr', 'wc', 'cfsr', 'ncar'],
      clabel   = u'air temperature (°C)',
      output   = 'cordillera-climate-temp',
      func     = func)

def prec():
    """Plot precipitation maps"""

    seasons  = ['djf']*3 + ['jja'] + ['djf']*2

    def func(i, clim):
      nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
      plt.title('%s %s' % (labels[clim], seasons[i].upper()))
      var = nc.variables['precipitation']
      if seasons[i] == 'jja': data = (var[5]  + var[6] + var[7]).T/3
      if seasons[i] == 'djf': data = (var[11] + var[0] + var[1]).T/3
      return plt.imshow(data,
        cmap = plt.cm.YlGnBu,
        norm = mcolors.LogNorm(0.1, 10))

    _plot_maps(
      climates = ['wc', 'erai', 'narr', 'wc', 'cfsr', 'ncar'],
      clabel   = u'precipitation rate (m/yr)',
      output   = 'cordillera-climate-prec',
      func     = func)

def topo():
    """Plot topography maps"""

    def func(i, clim):
      plt.title(labels[clim])
      if clim == 'etopo':
        nc = Dataset(pismdir + '/input/boot/cordillera-etopo1bed-10km.nc')
        return plt.imshow(nc.variables['topg'][:].T,
          cmap = icm.topo,
          norm = mcolors.Normalize(-6000, 6000))
      else:
        nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
        return plt.imshow(nc.variables['usurf'][:].T,
          cmap = icm.land_topo,
          norm = mcolors.Normalize(0, 6000))

    _plot_maps(
      climates = ['wc', 'erai', 'narr', 'etopo', 'cfsr', 'ncar'],
      clabel   = u'surface topography (m)',
      output   = 'cordillera-climate-topo',
      func     = func, ci = 3)

### Results plotting functions ###

def _plot_icemaps(climates, offsets, title, output, margin=False):
    """Base function to plot icemaps and LGM margin"""

    def func(i, clim):
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      plt.title(title % {'label': labels[clim], 'dt': offsets[i]})
      return iplt.icemap(nc)

    _plot_maps(climates, 'ice surface velocity (m/s)', output, func, margin=margin)

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
      output   = 'cordillera-climate-best',
      margin   = True)

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

def ivolarea():
    """Plot volume and area curves"""

    # initialize figure
    mm = 1/25.4
    figw = 85.
    figh = 60.
    fig = plt.figure(figsize=(figw*mm,figh*mm))
    ax1 = plt.axes([10/figw, 10/figh, 30/figw, 30/figh])
    ax2 = plt.axes([50/figw, 10/figh, 30/figw, 30/figh])
    ax1.set_xlabel('Temperature offset')
    ax1.set_ylabel(u'Glaciated area ($\mathsf{10^6~km^2}$)')
    ax2.set_xlabel('Temperature offset')
    ax2.set_ylabel(u'Ice volume ($\mathsf{10^6~km^3}$)')

    # select input data
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    coolings = range(10)

    # read input data
    for clim in climates:
      iarea = []
      ivol  = []
      for cool in coolings:
        nc = Dataset('../data/%s-%02g.nc' % (clim, cool))
        iarea.append((nc.variables['thk'][0]>1).sum()/1e4)
        nc = Dataset('../data/%s-%02g-ts.nc' % (clim, cool))
        ivol.append(nc.variables['ivol'][-1]/1e15)

      # plot
      ax1.plot(coolings, iarea, '.-')
      ax2.plot(coolings, ivol, '.-')

    # add legend
    ax2.legend(
      [labels[clim] for clim in climates],
      bbox_to_anchor = (10/figw, 45/figh, 70/figw, 10/figh),
      bbox_transform=fig.transFigure,
      loc=3, ncol=2, mode="expand", borderaxespad=0.)

    # save
    output = 'cordillera-climate-ivolarea'
    fig.savefig('cordillera-climate-ivolarea.png')
    fig.savefig('cordillera-climate-ivolarea.pdf')

### Command-line interface ###

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--temp', action='store_true',
      help='plot input temperature maps')
    parser.add_argument('--prec', action='store_true',
      help='plot input precipitation maps')
    parser.add_argument('--topo', action='store_true',
      help='plot input topography maps')
    parser.add_argument('--cool',
      help='plot icemaps for given temperature offset')
    parser.add_argument('--best', action='store_true',
      help='plot icemaps for so-called best runs')
    parser.add_argument('--extent', action='store_true',
      help='plot stacked ice extent from all runs')
    parser.add_argument('--ivolarea', action='store_true',
      help='plot colume and area curves')
    args = parser.parse_args()

    if args.temp is True: temp()
    if args.prec is True: prec()
    if args.topo is True: topo()
    if args.cool is not None: cool(args.cool)
    if args.best is True: best()
    if args.extent is True: extent()
    if args.ivolarea is True: ivolarea()


