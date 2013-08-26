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

### Base functions ###

def _seasonmean(var, season):
    if season == 'jja': data = (var[5]  + var[6] + var[7]).T/3
    if season == 'djf': data = (var[11] + var[0] + var[1]).T/3
    return np.ma.masked_equal(data, 0)

def _savefig(output):
    print 'saving ' + output
    plt.savefig(output + '.png')
    plt.savefig(output + '.pdf')

### Climate plotting functions ###

def temp():
    """Plot air temperature maps"""

    # initialize figure
    climates = ['wc', 'erai', 'narr', 'wc', 'cfsr', 'ncar']
    seasons  = ['jja']*3 + ['djf'] + ['jja']*2
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
      plt.title('%s %s' % (labels[clim], seasons[i].upper()))
      var = nc.variables['air_temp']
      data = _seasonmean(var, seasons[i])
      im = plt.imshow(data - 273.15,
        cmap = plt.cm.Spectral_r,
        norm = mcolors.Normalize(-30, 30))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'air temperature (°C)')
    _savefig('cordillera-climate-temp')

def tempdiff():
    """Plot temperaturedifference maps"""

    # initialize figure
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # read WorldClim data as reference
    nc = Dataset(pismdir + '/input/atm/cordillera-wc-10km-nn.nc')
    var = nc.variables['air_temp']
    ref = _seasonmean(var, 'jja')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
      plt.title(labels[clim])
      var = nc.variables['air_temp']
      data = _seasonmean(var, 'jja')
      im = plt.imshow(data - ref,
        cmap = plt.cm.RdBu_r,
        norm = mcolors.Normalize(-10, 10),
        )

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0], ticks=None)
    cb.set_label(u'JJA air temperature difference to WorldClim data (°C)')
    _savefig('cordillera-climate-tempdiff')

def prec():
    """Plot precipitation maps"""

    # initialise figure
    climates = ['wc', 'erai', 'narr', 'wc', 'cfsr', 'ncar']
    seasons  = ['djf']*3 + ['jja'] + ['djf']*2
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
      plt.title('%s %s' % (labels[clim], seasons[i].upper()))
      var = nc.variables['precipitation']
      data = _seasonmean(var, seasons[i])
      im = plt.imshow(data,
        cmap = plt.cm.YlGnBu,
        norm = mcolors.LogNorm(0.1, 10))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'precipitation rate (m/yr)')
    _savefig('cordillera-climate-prec')

def precdiff():
    """Plot precipitation difference maps"""

    # initialize figure
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # read WorldClim data as reference
    nc = Dataset(pismdir + '/input/atm/cordillera-wc-10km-nn.nc')
    var = nc.variables['precipitation']
    ref = _seasonmean(var, 'djf')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
      plt.title(labels[clim])
      var = nc.variables['precipitation']
      data = _seasonmean(var, 'djf')
      im = plt.imshow(data/ref-1 ,
        cmap = plt.cm.PuOr,
        norm = mcolors.Normalize(-2, 2))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0], ticks=None)
    cb.set_label(u'normalized DJF precipitation rate difference to WorldClim data')
    _savefig('cordillera-climate-precdiff')

def topo():
    """Plot topography maps"""

    # initialise figure
    climates = ['wc', 'erai', 'narr', 'etopo', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      plt.title(labels[clim])
      if clim == 'etopo':
        nc = Dataset(pismdir + '/input/boot/cordillera-etopo1bed-10km.nc')
        im = plt.imshow(nc.variables['topg'][:].T,
          cmap = icm.topo,
          norm = mcolors.Normalize(-6000, 6000))
      else:
        nc = Dataset(pismdir + '/input/atm/cordillera-%s-10km-nn.nc' % clim)
        plt.imshow(nc.variables['usurf'][:].T,
          cmap = icm.land_topo,
          norm = mcolors.Normalize(0, 6000))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'surface topography (m)')
    _savefig('cordillera-climate-topo')

### Results plotting functions ###

def best():
    """Plot icemaps for the best runs"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    offsets  = ['08', '06', '07', '04', '04', '04']
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='none')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      plt.title('%s - %s K' % (labels[clim], offsets[i]))
      iplt.bedtopoimage(nc)
      iplt.icemargincontour(nc, linecolors=None, colors='white', alpha=0.5)
      iplt.icemargincontour(nc)
      cs = iplt.surftopocontour(nc)

    # add LGM ice margin
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
    for ax in fig.grid:
      lines = LineCollection([data,], antialiaseds=(1,), colors='#000080')
      lines.zorder=0.5
      ax.add_collection(lines)

    # add colorbar and save
    cb = fig.colorbar(cs, fig.grid.cbar_axes[0])
    cb.set_label(u'ice surface velocity (m/s)')
    _savefig('cordillera-climate-best')

def bestdiff():
    """Plot differences in ice thickness for the best runs"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    offsets  = ['09', '07', '08', '05', '05', '04']
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      plt.title('%s - %s K' % (labels[clim], offsets[i]))
      data = nc.variables['usurf'][0].T
      if i == 0:
        ref = data
        im = iplt.icemap(nc)
      else:
        im = plt.imshow(data - ref,
          cmap = plt.cm.RdBu,
          norm = mcolors.Normalize(-3000, 3000))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'ice surface elevation difference to %s %s K simulation (m)' % (labels[climates[0]], offsets[0]))
    _savefig('cordillera-climate-bestdiff')

def cool(cool):
    """Plot icemaps for given temperature offset"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    offsets  = [cool]*6
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      plt.title(labels[clim])
      im = iplt.icemap(nc)

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'ice surface velocity (m/s)')
    _savefig('cordillera-climate-cool' + cool)

def extent():
    """Plot stacked ice extents"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, len(climates)/2), cbar_mode='single')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      plt.title(labels[clim])
      icecover = 11
      for dt in range(10,-1,-1):
        nc = Dataset('../data/%s-%02g.nc' % (clim, dt))
        icecover = np.where(nc.variables['thk'][0] > 1, dt, icecover)
      #cs = plt.contour(icecover.T,
      #  levels = range(0, 11),
      #  colors = 'black',
      #  linewidths = 0.2)
      cs = plt.contourf(icecover.T,
        levels = range(-1, 11),
        cmap   = plt.cm.Blues_r)

    # add colorbar and save
    cb = fig.colorbar(cs, fig.grid.cbar_axes[0], ticks=range(11))
    cb.set_label(u'temperature offset (°C)')
    _savefig('cordillera-climate-extent')

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
    coolings = range(11)

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
    parser.add_argument('--tempdiff', action='store_true',
      help='plot input temperature difference maps')
    parser.add_argument('--prec', action='store_true',
      help='plot input precipitation maps')
    parser.add_argument('--precdiff', action='store_true',
      help='plot input precipitation difference maps')
    parser.add_argument('--topo', action='store_true',
      help='plot input topography maps')
    parser.add_argument('--cool',
      help='plot icemaps for given temperature offset')
    parser.add_argument('--best', action='store_true',
      help='plot icemaps for so-called best runs')
    parser.add_argument('--bestdiff', action='store_true',
      help='plot ice thickness difference for the best runs')
    parser.add_argument('--extent', action='store_true',
      help='plot stacked ice extent from all runs')
    parser.add_argument('--ivolarea', action='store_true',
      help='plot colume and area curves')
    args = parser.parse_args()

    if args.temp     is True: temp()
    if args.tempdiff is True: tempdiff()
    if args.prec     is True: prec()
    if args.precdiff is True: precdiff()
    if args.topo     is True: topo()
    if args.cool is not None: cool(args.cool)
    if args.best     is True: best()
    if args.bestdiff is True: bestdiff()
    if args.extent   is True: extent()
    if args.ivolarea is True: ivolarea()


