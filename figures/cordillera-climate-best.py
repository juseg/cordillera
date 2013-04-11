#!/usr/bin/env python
# coding: utf-8

#import matplotlib as mpl
#mpl.use('Agg')
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from pismplot.figure import gridfigure
from pismplot.datasets import Extra

# select input data
climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
labels   = ['WorldClim', 'ERA-Interim', 'NARR', 'smoothed CFSR', 'CFSR', 'NCEP/NCAR']
coolings = [9, 7, 8, 5, 5, 4]

# icemaps
fig = gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')
for i in range(len(climates)):
	clim  = climates[i]
	label = labels[i]
	cool  = coolings[i]

	# plot
	print 'drawing %s cool%02i...' % (clim, cool)
	nc = Extra('../../../output/cordillera-%s-10km-bl/stepcool%02dsll120+lc+tcalv200+pik+gflx70+ssa+till1030/y0010000-extra.nc' % (clim, cool))
	nc.map.ax=fig.grid[i]
	im = nc._drawicemap(99)
	nc.map.ax.set_title('%s - %02i K' % (label, cool))

	# colorbar
	cb = fig.colorbar(im, fig.grid.cbar_axes[0])
	cb.set_label('ice surface velocity (m/yr)')

# save
output = 'cordillera-climate-best'
fig.vsavefig(output + '.png')
fig.vsavefig(output + '.pdf')

