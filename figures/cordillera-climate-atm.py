#!/usr/bin/env python
# coding: utf-8

#import matplotlib as mpl
#mpl.use('Agg')
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from pismplot.datasets import Atm
from pismplot.figure import gridfigure
from pismplot.names import names

# select input data
climates = ['ncar', 'cfsr', 'narr', 'erai', 'cfsrs7', 'wcnn']
labels   = ['NCEP/NCAR', 'CFSR', 'NCEP/NARR', 'ERA-Interim', 'CFSR smoothed', 'WorldClim']
methods  = ['nn', 'bl']
variables= ['air_temp', 'precipitation']
seasons  = ['djf', 'jja']

# for each interpolation method
for met in methods:

	# topography maps
	fig = gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')
	for i in range(len(climates)):
				clim  = climates[i]
				label = labels[i]

				# plot
				print 'drawing %s reference topography...' % clim
				nc = Atm('../../../input/atm/cordillera-%s-10km-%s.nc' % (clim, met))
				nc.map.ax=fig.grid[i]
				nc._drawgrats()
				im = nc._drawimage('usurf')
				nc.map.ax.set_title(label)

				# colorbar
				cb = fig.colorbar(im, fig.grid.cbar_axes[0])
				cb.set_label('Reference topography (m)')

	# save
	output = 'cordillera-climate-usurf-%s' % met
	fig.vsavefig(output + '.png')
	fig.vsavefig(output + '.pdf')

	# temperature and precipitation maps
	for var in variables:
		for t in seasons:
			fig = gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')

			# for each climate dataset
			for i in range(len(climates)):
				clim  = climates[i]
				label = labels[i]

				# plot
				print 'drawing %s %s %s...' % (clim, t.upper(), names[var])
				nc = Atm('../../../input/atm/cordillera-%s-10km-%s.nc' % (clim, met))
				nc.map.ax=fig.grid[i]
				im = nc._drawseasonalmap(var, t)
				nc.map.ax.set_title(label)

				# colorbar
				cb = fig.colorbar(im, fig.grid.cbar_axes[0])
				cb.set_label(t.upper() + ' ' + names[var])

			# save
			output = 'cordillera-climate-%s-%s-%s' % (var, t, met)
			fig.vsavefig(output + '.png')
			fig.vsavefig(output + '.pdf')

