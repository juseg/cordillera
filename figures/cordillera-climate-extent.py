#!/usr/bin/env python
# coding: utf-8

#import matplotlib as mpl
#mpl.use('Agg')
from numpy import where
from matplotlib import pyplot as plt
from pismplot.dataset import PismDataset as NC
from pismplot.icemap import Icemap
from pismplot.figure import gridfigure

# select input data
climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
labels   = ['WorldClim', 'ERA-Interim', 'NARR', 'smoothed CFSR', 'CFSR', 'NCEP/NCAR']
coolings = range(2, 10)

# initialize
fig = gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')
m = None
(x, y) = (None, None)

for i in range(len(climates)):
	clim  = climates[i]
	label = labels[i]
	print 'drawing %s ice cover...' % clim
	icecover = 0

	# stack ice covers from all simulations
	for cool in reversed(coolings):
		nc = NC('../../../output/cordillera-%s-10km-bl/stepcool%02dsll120+lc+tcalv200+pik+gflx70+ssa+till1030/y0010000-extra.nc' % (clim, cool))
		m = m or Icemap(nc)
		#icecover += ( nc.get_timeframe('thk', 99) > 1 )
		#icecover = ( cool if ( nc.var['thk'][99] > 1 ) else icecover)
		icecover = where(nc.var['thk'][99] > 1, cool, icecover)

	# draw ice cover
	m.ax=fig.grid[i]
	(x, y) = m(nc.get_timeframe('lon'), nc.get_timeframe('lat'))
	m.drawgraticules()
	cs = m.contourf(x, y, icecover.T,
			levels = range(1,10),
			cmap   = plt.cm.Blues_r)
	m.ax.set_title(label)

# colorbar
cb = fig.colorbar(cs, fig.grid.cbar_axes[0])
cb.set_label(u'temperature offset (°C)')

# save
output = 'cordillera-climate-extent'
fig.vsavefig(output + '.png')
fig.vsavefig(output + '.pdf')

