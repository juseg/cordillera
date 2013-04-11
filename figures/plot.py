#!/usr/bin/env python
# coding: utf-8

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from iceplot import plot as iplt

# select input data
climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
labels   = ['WorldClim', 'ERA-Interim', 'NARR', 'smoothed CFSR', 'CFSR', 'NCEP/NCAR']

# given temperature offset
def cool(cool):
  	fig = iplt.gridfigure((30., 60.), (2, len(climates)/2), cbar_mode='single')
  	for i in range(len(climates)):
  		clim  = climates[i]
  		label = labels[i]
  
  		# plot
  		print 'drawing %s cool%s...' % (clim, cool)
  		nc = Dataset('../data/%s-%s.nc' % (clim, cool))
  		ax = plt.axes(fig.grid[i])
  		im = iplt.icemap(nc)
  		ax.set_title(label)
  
  		# colorbar
  		cb = fig.colorbar(im, fig.grid.cbar_axes[0])
  		cb.set_label('ice surface velocity (m/yr)')
  
  	# save
  	output = 'cordillera-climate-cool%s' % cool
  	fig.savefig(output + '.png')
  	fig.savefig(output + '.pdf')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cool',
      help='plot icemaps for given temperature offset')
    args = parser.parse_args()

    if args.cool is not None: cool(args.cool)


