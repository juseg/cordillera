#!/usr/bin/env python
# coding: utf-8

import os
#import matplotlib as mpl
#mpl.use('Agg')
from matplotlib import pyplot as plt
from netCDF4 import Dataset

# set matplotlib configuration
plt.rc('font', size=6)
plt.rc('savefig', dpi=254)

# initialize figure
mm = 1/25.4
axw = 32.5
axh = 32.5
pad = 10.
lgh = 7.5
lgpad = 5.
figw = 2*axw + 2.5*pad
figh =   axh + pad +lgh +2*lgpad
fig = plt.figure(figsize=(figw*mm,figh*mm))
ax1 = plt.axes([        pad/figw, pad/figh, axw/figw, axh/figh])
ax2 = plt.axes([(axw+2*pad)/figw, pad/figh, axw/figw, axh/figh])

# select input data
climates = ['wcnn', 'erai', 'narr', 'cfsrs7', 'cfsr', 'ncar']
labels   = ['WorldClim', 'ERA-Interim', 'NARR', 'smoothed CFSR', 'CFSR', 'NCEP/NCAR']
coolings = range(2,10)

# read input data
for clim in climates:
	iarea = []
	ivol  = []
	for cool in coolings:
		nc = Dataset('../../../output/cordillera-%s-10km-bl/stepcool%02dsll120+lc+tcalv200+pik+gflx70+ssa+till1030/y0010000-ts.nc' % (clim, cool))
		iarea.append(nc.variables['iarea'][-1]/1e12)
		ivol.append(nc.variables['ivol'][-1]/1e15)

	# plot
	ax1.plot(coolings, iarea, '.-')
	ax2.plot(coolings, ivol, '.-')

# set labels and legend
ax1.set_xlabel('Temperature offset')
ax1.set_ylabel(u'Glaciated area (10⁶ km²)')
ax2.set_xlabel('Temperature offset')
ax2.set_ylabel(u'Ice volume (10⁶ km³)')
ax2.legend(labels,
	bbox_to_anchor = (pad/figw, (pad+axh+lgpad)/figh, 1-1.5*pad/figw, pad/figh), bbox_transform=fig.transFigure,
	loc=3, ncol=2, mode="expand", borderaxespad=0.)

# save
plt.savefig('cordillera-climate-ivolarea.png')
plt.savefig('cordillera-climate-ivolarea.pdf')

