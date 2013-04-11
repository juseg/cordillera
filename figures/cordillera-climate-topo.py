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
climates = ['wc', 'erai', 'narr', 'etopo', 'cfsr', 'ncar']
var = 'usurf'
met = 'nn'

# initialize figure
fig = gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')
m = None

# for each climate dataset
for i, clim in enumerate(climates):

	# plot
	if clim == 'etopo':
		print 'drawing ETOPO1 topography...'
		nc = NC('../../../input/boot/cordillera-etopo1bed-10km.nc')
		m.ax=fig.grid[i]
		m.drawgraticules()
		im = m.drawimage('topg', nc=nc)
		m.ax.set_title('ETOPO1')
	else:
		print 'drawing %s %s...' % (clim, names[var])
		nc = NC('../../../input/atm/cordillera-%s-10km-%s.nc' % (clim, met))
		m = m or Icemap(nc)
		m.ax=fig.grid[i]
		m.drawgraticules()
		m.drawimage(var, nc=nc)
		m.ax.set_title(labels[clim])

# colorbar
cb = fig.colorbar(im, fig.grid.cbar_axes[0])
#cb.set_label(names[var])

# save
output = 'cordillera-climate-topo'
fig.vsavefig(output + '.png')
fig.vsavefig(output + '.pdf')

