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

mm = 1/25.4
mapsize = (30., 60.)
figkwa = dict(axes_pad=2*mm, cbar_pad=2*mm, cbar_size=4*mm)
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

def _annotate(text):
    plt.text(140, 290, text,
      verticalalignment='top',
      horizontalalignment='right',
      bbox=dict(ec='none', fc='w', alpha=0.75))

def _drawlgm(nc, grid,**kwargs):
    """Add LGM ice margin from Dyke (2004)"""
    from matplotlib.patches import Polygon
    m = Basemap(projection='lcc',
      lat_1=49, lat_2=77, lat_0=49, lon_0=-95,
      llcrnrlat=nc.variables['lat'][0,0],
      urcrnrlat=nc.variables['lat'][-1,-1],
      llcrnrlon=nc.variables['lon'][0,0],
      urcrnrlon=nc.variables['lon'][-1,-1])
    sf = shapefile.Reader('../data/16.8-ka.shp')
    for ax in grid:
      for shape in sf.shapes():
        lons,lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T/10000
        poly = Polygon(data, **kwargs)
        ax.add_patch(poly)

def _seasonmean(var, season):
    if season == 'jja': data = (var[5]  + var[6] + var[7]).T/3
    if season == 'djf': data = (var[11] + var[0] + var[1]).T/3
    return np.ma.masked_equal(data, 0)

def _savefig(output, png=True, pdf=True):
    print 'saving ' + output
    if png: plt.savefig(output + '.png')
    if pdf: plt.savefig(output + '.pdf')

### Climate plotting functions ###

def temp():
    """Plot air temperature maps"""

    # initialize figure
    climates = ['wc', 'erai', 'narr', 'wc', 'cfsr', 'ncar']
    seasons  = ['jja']*3 + ['djf'] + ['jja']*2
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-nn.nc' % clim)
      _annotate('%s %s' % (labels[clim], seasons[i].upper()))
      var = nc.variables['air_temp']
      data = _seasonmean(var, seasons[i])
      im = plt.imshow(data - 273.15,
        cmap = plt.cm.Spectral_r,
        norm = mcolors.Normalize(-30, 30))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'air temperature (°C)')
    _savefig('cordillera-climate-temp')

def tempbox():
    """Plot air temperature boxes"""

    # initialize figure
    climates = ['wc', 'erai', 'narr', 'cfsr', 'ncar']
    data = []

    # plot
    for clim in climates:
      nc = Dataset('../data/%s-nn.nc' % clim)
      var = nc.variables['air_temp']
      tmp = _seasonmean(var, 'jja') - 273.15
      if clim != 'wc': tmp = np.ma.masked_where(data[0].mask, tmp)
      data.append(tmp)
    data = map(np.ma.compressed, data)
    plt.boxplot(data)

    # save
    _savefig('cordillera-climate-tempbox')

def tempdiff():
    """Plot temperature difference maps"""

    # initialize figure
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, 2), cbar_mode='single', **figkwa)

    # read WorldClim data as reference
    nc = Dataset('../data/wc-nn.nc')
    var = nc.variables['air_temp']
    ref = _seasonmean(var, 'jja')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-bl.nc' % clim)
      _annotate(labels[clim])
      var = nc.variables['air_temp']
      data = _seasonmean(var, 'jja')
      im = plt.imshow(data - ref,
        cmap = plt.cm.RdBu_r,
        norm = mcolors.Normalize(-10, 10))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0], ticks=None)
    cb.set_label(u'JJA air temperature difference to WorldClim data (°C)')
    _savefig('cordillera-climate-tempdiff')

def tempheatmap():
    """Plot temperature heat maps"""

    from mpl_toolkits.axes_grid1 import ImageGrid

    # climate datasets
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    fig = plt.figure(figsize=(85/25.4, 85/25.4))
    grid = ImageGrid(fig, [ 8/85.,  4/85., 75/85., 75/85.],
      nrows_ncols=(2, 2), axes_pad=2/25.4, label_mode = "1")

    # read WorldClim data as reference
    nc = Dataset('../data/wc-nn.nc')
    var = nc.variables['air_temp']
    ref = _seasonmean(var, 'jja') - 273.15
    refdata = ref.compressed()

    # loop on climate datasets
    for clim, ax in zip(climates, grid):

      # read other data
      nc = Dataset('../data/%s-nn.nc' % clim)
      var = nc.variables['air_temp']
      data = _seasonmean(var, 'jja') - 273.15
      data = np.ma.array(data, mask=ref.mask).compressed()

      # plot
      minmax = (-5, 25)
      ax.hist2d(refdata, data,
        range=(minmax, minmax), bins=120,
        cmap=plt.cm.Reds, norm=mcolors.LogNorm())
      #ax.scatter(refdata, data, c='r', marker='o', alpha=0.002)
      ax.plot(minmax, minmax,'k')

      # set axes properties
      ax.set_xlim(minmax)
      ax.set_ylim(minmax)
      ax.text(-3, 22, labels[clim])
      ax.text(15, -3, labels['wc'])

      # calc mean deviation
      print (data-refdata).mean()

    # save
    fig.suptitle(u'JJA mean surface air temperature (°C)')
    _savefig('cordillera-climate-tempheatmap', pdf=True)

def prec():
    """Plot precipitation maps"""

    # initialise figure
    climates = ['wc', 'erai', 'narr', 'wc', 'cfsr', 'ncar']
    seasons  = ['djf']*3 + ['jja'] + ['djf']*2
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-nn.nc' % clim)
      _annotate('%s %s' % (labels[clim], seasons[i].upper()))
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
    fig = iplt.gridfigure(mapsize, (2, 2), cbar_mode='single', **figkwa)

    # read WorldClim data as reference
    nc = Dataset('../data/wc-nn.nc')
    var = nc.variables['precipitation']
    ref = _seasonmean(var, 'djf')

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-bl.nc' % clim)
      _annotate(labels[clim])
      var = nc.variables['precipitation']
      data = _seasonmean(var, 'djf')
      im = plt.imshow(data/ref-1 ,
        cmap = plt.cm.PuOr,
        norm = mcolors.Normalize(-2, 2))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0], ticks=None)
    cb.set_label(u'normalized DJF precipitation rate difference to WorldClim data')
    _savefig('cordillera-climate-precdiff')

def precheatmap():
    """Plot precipitation heat maps"""

    from matplotlib.ticker import FormatStrFormatter
    from mpl_toolkits.axes_grid1 import ImageGrid

    # climate datasets
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    fig = plt.figure(figsize=(85/25.4, 85/25.4))
    grid = ImageGrid(fig, [ 8/85.,  4/85., 75/85., 75/85.],
      nrows_ncols=(2, 2), axes_pad=2/25.4, label_mode = "1")

    # read WorldClim data as reference
    nc = Dataset('../data/wc-nn.nc')
    var = nc.variables['precipitation']
    ref = _seasonmean(var, 'djf')
    refdata = ref.compressed()

    # loop on climate datasets
    for clim, ax in zip(climates, grid):

      # read other data
      nc = Dataset('../data/%s-nn.nc' % clim)
      var = nc.variables['precipitation']
      data = _seasonmean(var, 'djf')
      data = np.ma.array(data, mask=ref.mask).compressed()

      # plot
      minmax = (0.01, 10)
      hist, x, y = np.histogram2d(np.log10(refdata), np.log10(data),
        range=np.log10((minmax, minmax)), bins=120)
      ax.imshow(hist.T,
        cmap=plt.cm.Blues, norm=mcolors.LogNorm(),
        extent=[0.01, 10, 0.01, 10])
      #ax.scatter(refdata, data, marker='o', alpha=0.002)
      ax.plot(minmax, minmax,'k')

      # set axes properties
      ax.set_xlim(minmax)
      ax.set_ylim(minmax)
      ax.set_xscale('log')
      ax.set_yscale('log')
      ax.xaxis.set_major_formatter(FormatStrFormatter('%g'))
      ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))
      ax.text(0.015, 5, labels[clim])
      ax.text(1, 0.015, labels['wc'])

      # calc mean deviation
      print (data-refdata).mean()

    # save
    fig.suptitle('DJF mean precipitation rate (m/yr)')
    _savefig('cordillera-climate-precheatmap', pdf=True)

def topo():
    """Plot topography maps"""

    # initialise figure
    climates = ['wc', 'erai', 'narr', 'etopo', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      _annotate(labels[clim])
      if clim == 'etopo':
        nc = Dataset('../data/etopo1bed.nc')
        im = plt.imshow(nc.variables['topg'][:].T,
          cmap = icm.topo,
          norm = mcolors.Normalize(-6000, 6000))
      else:
        nc = Dataset('../data/%s-nn.nc' % clim)
        plt.imshow(nc.variables['usurf'][:].T,
          cmap = icm.land_topo,
          norm = mcolors.Normalize(0, 6000))

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'surface topography (m)', labelpad=-5)
    _savefig('cordillera-climate-topo')

### Results plotting functions ###

def best():
    """Plot icemaps for the best runs"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    offsets  = ['08', '06', '07', '04', '04', '04']
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='none', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      _annotate('%s - %s K' % (labels[clim], offsets[i]))
      iplt.bedtopoimage(nc)
      iplt.icemargincontour(nc, linecolors=None, colors='white', alpha=0.5)
      iplt.icemargincontour(nc)
      cs = iplt.surftopocontour(nc)

    # add LGM ice margin, colorbar and save
    _drawlgm(nc, fig.grid, edgecolor='#000080', facecolor='none', zorder=0.5)
    cb = fig.colorbar(cs, fig.grid.cbar_axes[0])
    cb.set_label(u'ice surface velocity (m/s)')
    _savefig('cordillera-climate-best')

def bestdiff():
    """Plot differences in ice thickness for the best runs"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    offsets  = ['09', '07', '08', '05', '05', '04']
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      _annotate('%s - %s K' % (labels[clim], offsets[i]))
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

def biatm():
    """Plot hybrid atmosphere output"""

    # initialize figure
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, 4), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      for j, biclim in enumerate(['t%spwcnn' % clim, 'twcnnp%s' % clim]):
        ax = plt.axes(fig.grid[i+4*j])
        if j==0: _annotate(labels[clim] + ' temperature')
        if j==1: _annotate(labels[clim] + ' precipitation')
        nc = Dataset('../data/%s-05.nc' % biclim)
        im = iplt.icemap(nc)

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'ice surface velocity (m/s)')
    _savefig('cordillera-climate-biatm')

def biatmbars():
    """Plot hybrid atmosphere bar chart"""

    # climate datasets
    climates = ['erai', 'narr', 'cfsr', 'ncar']
    both = []; temp = []; prec = []

    # read reference data (volume)
    nc = Dataset('../data/wcnn-05-ts.nc')
    ref = nc.variables['ivol'][-1]/1e15

    # read reference data (area)
    #nc = Dataset('../data/wcnn-05.nc')
    #ref = (nc.variables['thk'][0]).sum()/1e4

    # read other data (volume)
    for i, clim in enumerate(climates):
      nc = Dataset('../data/%s-05-ts.nc' % clim)
      both.append(nc.variables['ivol'][-1]/1e15)
      nc = Dataset('../data/t%spwcnn-05-ts.nc' % clim)
      temp.append(nc.variables['ivol'][-1]/1e15)
      nc = Dataset('../data/twcnnp%s-05-ts.nc' % clim)
      prec.append(nc.variables['ivol'][-1]/1e15)

    # read other data (area)
    #for i, clim in enumerate(climates):
    #  nc = Dataset('../data/%s-05.nc' % clim)
    #  both.append((nc.variables['thk'][0]).sum()/1e4)
    #  nc = Dataset('../data/t%spwcnn-05.nc' % clim)
    #  temp.append((nc.variables['thk'][0]).sum()/1e4)
    #  nc = Dataset('../data/twcnnp%s-05.nc' % clim)
    #  prec.append((nc.variables['thk'][0]).sum()/1e4)

    # initialize figure
    w = 0.25
    pos = np.arange(len(climates)) - w/2
    fig = plt.figure(figsize=(85*mm, 60*mm))
    ax = plt.axes([10/85., 5/60., 73/85., 53/60.])

    # plot bars
    barkwargs = {'linewidth': 0.2, 'alpha': 0.5}
    ax.bar(pos, both-ref, w, color='#333333',
      label='cumulative', **barkwargs)
    ax.bar(pos-w/2, temp-ref, w, color='#ff3333',
      label='temperature', **barkwargs)
    ax.bar(pos+w/2, prec-ref, w, color='#3333ff',
      label='precipitation', **barkwargs)

    # adjust axes
    plt.axhline(0, color='k', linewidth=0.2)
    plt.xticks(pos+w/2, [labels[clim] for clim in climates])
    plt.ylabel(u'Ice volume anomaly ($\mathsf{10^6~km^3}$)')
    plt.legend(loc=2)
    #plt.ylabel(u'Glaciated area anomaly ($\mathsf{10^6~km^2}$)')

    # save
    _savefig('cordillera-climate-biatmbars')

def cool(cool):
    """Plot icemaps for given temperature offset"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    offsets  = [cool]*6
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      nc = Dataset('../data/%s-%s.nc' % (clim, offsets[i]))
      _annotate(labels[clim])
      im = iplt.icemap(nc)

    # add colorbar and save
    cb = fig.colorbar(im, fig.grid.cbar_axes[0])
    cb.set_label(u'ice surface velocity (m/s)')
    _savefig('cordillera-climate-cool' + cool)

def duration():
    """Plot effect of glaciation duration on multiple maps"""

    # initialize figure
    clim = 'narr'
    alloffsets = range(16)
    mapoffsets = range(7, 12)
    tarea = 2.1823
    lgmtimes = []
    figw, figh = 115., 135.
    fig = plt.figure(figsize=(figw*mm, figh*mm))
    grid = [
      fig.add_axes([10/figw, 70/figh, 30/figw, 60/figh]),
      fig.add_axes([45/figw, 70/figh, 30/figw, 60/figh]),
      fig.add_axes([80/figw, 70/figh, 30/figw, 60/figh]),
      fig.add_axes([10/figw,  5/figh, 30/figw, 60/figh]),
      fig.add_axes([45/figw,  5/figh, 30/figw, 60/figh]),
      fig.add_axes([80/figw,  5/figh, 30/figw, 60/figh])]

    # plot glaciatied area curves
    ax = plt.axes(grid[0])
    for dt in range(16):
      nc = Dataset('../data/%s-%02g-extra.nc' % (clim, dt))
      time = nc.variables['time'][1:] / 31556925974.7
      iarea = (nc.variables['thk'][1:]>10).sum(axis=(1, 2))/1e4
      plt.plot(time, iarea, ('b-' if dt in mapoffsets else 'b--'))
      lgmtimes.append((np.abs(iarea-tarea)).argmin())
    ax.set_xlim((0, 10))
    ax.set_ylim((0, 4))
    plt.plot([0, 100],[tarea, tarea], 'k')

    # plot maps
    for i, dt in enumerate(mapoffsets):
      ax = plt.axes(grid[i+1])
      ax.get_xaxis().set_visible(False)
      ax.get_yaxis().set_visible(False)
      nc = Dataset('../data/%s-%02g-extra.nc' % (clim, dt))
      iplt.bedtopoimage(nc, t=lgmtimes[dt])
      iplt.icemargincontour(nc, t=lgmtimes[dt],
        linecolors=None, colors='white', alpha=0.5)
      iplt.icemargincontour(nc, t=lgmtimes[dt])
      iplt.surftopocontour(nc, t=lgmtimes[dt])

    # add LGM ice margin and save
    _drawlgm(nc, grid[1:], edgecolor='#000080', facecolor='none', zorder=0.5)
    _savefig('cordillera-climate-duration')

def durationstack():
    """Plot effect of glaciation duration on a single map"""

    # initialize figure
    clim = 'narr'
    alloffsets = range(16)
    mapoffsets = range(7, 12)
    c = ['k']*7 + ['#ff3333', '#cc3366', '#993399', '#6633cc', '#3333ff'] + ['k']*4
    tarea = 2.1823
    lgmtimes = []
    figw, figh = 80., 70.
    fig = plt.figure(figsize=(figw*mm, figh*mm))
    grid = [
      fig.add_axes([10/figw, 5/figh, 30/figw, 60/figh]),
      fig.add_axes([45/figw, 5/figh, 30/figw, 60/figh])]

    # plot glaciatied area curves
    ax = plt.axes(grid[0])
    for dt in range(16):
      nc = Dataset('../data/%s-%02g-extra.nc' % (clim, dt))
      time = nc.variables['time'][1:] / 31556925974.7
      iarea = (nc.variables['thk'][1:]>10).sum(axis=(1, 2))/1e4
      plt.plot(time, iarea, ('-' if dt in mapoffsets else '--'), color=c[dt])
      lgmtimes.append((np.abs(iarea-tarea)).argmin())
    ax.set_xlim((0, 10))
    ax.set_ylim((0, 4))
    plt.plot([0, 100],[tarea, tarea], 'k')

    # plot maps
    ax = plt.axes(grid[1])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for dt in mapoffsets:
      nc = Dataset('../data/%s-%02g-extra.nc' % (clim, dt))
      iplt.icemargincontour(nc, t=lgmtimes[dt], linecolors=c[dt])

    # add LGM ice margin and save
    _drawlgm(nc, [ax], facecolor='#cccccc', linewidth=0)
    _savefig('cordillera-climate-durationstack')

def extent():
    """Plot stacked ice extents"""

    # initialize figure
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    fig = iplt.gridfigure(mapsize, (2, 3), cbar_mode='single', **figkwa)

    # loop on climate datasets
    for i, clim in enumerate(climates):
      ax = plt.axes(fig.grid[i])
      _annotate(labels[clim])
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
        cmap   = plt.cm.Spectral)

    # add colorbar and save
    cb = fig.colorbar(cs, fig.grid.cbar_axes[0], ticks=range(11))
    cb.set_label(u'temperature offset (°C)')
    _savefig('cordillera-climate-extent')

def ivolarea():
    """Plot volume and area curves"""

    # initialize figure
    mm = 1/25.4
    figw = 85.
    figh = 56.
    fig = plt.figure(figsize=(figw*mm,figh*mm))
    ax1 = plt.axes([ 8/figw, 8/figh, 32/figw, 32/figh])
    ax2 = plt.axes([51/figw, 8/figh, 32/figw, 32/figh])
    ax1.set_xlabel('Temperature offset')
    ax1.set_ylabel(u'Glaciated area ($\mathsf{10^6~km^2}$)')
    #ax1.text(-1.5, 2, u'Glaciated area ($\mathsf{10^6~km^2}$)',
    #  rotation='vertical', va='center', ha='right')
    ax2.set_xlabel('Temperature offset')
    ax2.set_ylabel(u'Ice volume ($\mathsf{10^6~km^3}$)')
    #ax2.text(-1.5, 6, u'Ice volume ($\mathsf{10^6~km^3}$)',
    #  rotation='vertical', va='center', ha='right')

    # select input data
    climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
    styles   = ['s-', 'D-', 'o-', '^-', 'v-', 'h-']
    coolings = range(11)

    # read input data
    for clim, style in zip(climates, styles):
      iarea = []
      ivol  = []
      for cool in coolings:
        nc = Dataset('../data/%s-%02g.nc' % (clim, cool))
        iarea.append((nc.variables['thk'][0]>1).sum()/1e4)
        nc = Dataset('../data/%s-%02g-ts.nc' % (clim, cool))
        ivol.append(nc.variables['ivol'][-1]/1e15)

      # plot
      ax1.plot(coolings, iarea, style, mew=0, ms=3)
      ax2.plot(coolings, ivol, style, mew=0, ms=3)

    # add legend
    ax1.set_yticks(range(5))
    ax2.legend(
      [labels[clim] for clim in climates],
      bbox_to_anchor = (8/figw, 42/figh, 75/figw, 10/figh),
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
    parser.add_argument('--tempbox', action='store_true',
      help='plot input temperature boxes')
    parser.add_argument('--tempdiff', action='store_true',
      help='plot input temperature difference maps')
    parser.add_argument('--tempheatmap', action='store_true',
      help='plot input temperature heat maps')
    parser.add_argument('--prec', action='store_true',
      help='plot input precipitation maps')
    parser.add_argument('--precdiff', action='store_true',
      help='plot input precipitation difference maps')
    parser.add_argument('--precheatmap', action='store_true',
      help='plot input precipitation heat maps')
    parser.add_argument('--topo', action='store_true',
      help='plot input topography maps')
    parser.add_argument('--cool',
      help='plot icemaps for given temperature offset')
    parser.add_argument('--best', action='store_true',
      help='plot icemaps for so-called best runs')
    parser.add_argument('--bestdiff', action='store_true',
      help='plot ice thickness difference for the best runs')
    parser.add_argument('--biatm', action='store_true',
      help='plot hybrid atmosphere output')
    parser.add_argument('--biatmbars', action='store_true',
      help='plot hybrid atmosphere bar chart')
    parser.add_argument('--duration', action='store_true',
      help='plot effect of glaciation duration on multiple maps')
    parser.add_argument('--durationstack', action='store_true',
      help='plot effect of glaciation duration on a single map')
    parser.add_argument('--extent', action='store_true',
      help='plot stacked ice extent from all runs')
    parser.add_argument('--ivolarea', action='store_true',
      help='plot colume and area curves')
    args = parser.parse_args()

    if args.temp     is True: temp()
    if args.tempbox  is True: tempbox()
    if args.tempdiff is True: tempdiff()
    if args.tempheatmap is True: tempheatmap()
    if args.prec     is True: prec()
    if args.precdiff is True: precdiff()
    if args.precheatmap is True: precheatmap()
    if args.topo     is True: topo()
    if args.cool is not None: cool(args.cool)
    if args.best     is True: best()
    if args.bestdiff is True: bestdiff()
    if args.biatm    is True: biatm()
    if args.biatmbars is True: biatmbars()
    if args.extent   is True: extent()
    if args.duration is True: duration()
    if args.durationstack is True: durationstack()
    if args.ivolarea is True: ivolarea()


