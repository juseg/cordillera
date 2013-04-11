#!/usr/bin/env python
# coding: utf-8

#import matplotlib as mpl
#mpl.use('Agg')
from pismplot.dataset import PismMonthlyDataset as NC
from pismplot.icemap import Icemap
from pismplot.figure import gridfigure
from pismplot.names import names

# labels for climate datasets
labels   = {
	'cfsr': 'CFSR',
	'erai': 'ERA-Interim',
	'narr': 'NARR',
	'ncar': 'NCEP/NCAR',
	'wc':   'WorldClim'}

# select input data
climates = ['wc', 'erai' , 'narr', 'wc', 'cfsr', 'ncar']
seasons  = ['jja']*3 + ['djf'] + ['jja']*2
var = 'air_temp'
met = 'nn'

# initialize figure and map
fig = gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')
m = None

# for each climate dataset
for i, clim in enumerate(climates):
	t = seasons[i]

	# plot
	print 'drawing %s %s %s...' % (clim, t.upper(), names[var])
	nc = NC('../../../input/atm/cordillera-%s-10km-%s.nc' % (clim, met))
	m = m or Icemap(nc)
	m.ax=fig.grid[i]
	m.drawgraticules()
	im = m.drawimage(var, t, mask=((nc.get_timeframe(var, t) < -60) if clim == 'wc' else None), nc=nc)
	m.ax.set_title(labels[clim] + ' ' + t.upper())

# colorbar
cb = fig.colorbar(im, fig.grid.cbar_axes[0])
cb.set_label(names[var])

# save
output = 'cordillera-climate-temp'
fig.vsavefig(output + '.png')
fig.vsavefig(output + '.pdf')

