#!/usr/bin/env python2
# coding: utf-8

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as mplt
from iceplot import plot as iplt

# unit conversion
mm2in = 1/25.4
s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)

# file path
run_path = '/home/julien/pism/output/cordillera-narr-5km-bl/' \
           'grip3222cool580+ccyc+till1545/y0120000'

# use time series to locate glacial maximum
nc  = Dataset(run_path + '-ts.nc')
time = nc.variables['time']  #*s2ka
ivol = nc.variables['iarea']
lgm_indx = np.ma.argmax(ivol[:])
lgm_time = time[lgm_indx]
nc.close()
print lgm_indx, lgm_time*s2ka

# round lgm time to nearest slice
nc  = Dataset(run_path + '-extra--0021700.000.nc')
time = nc.variables['time']  #*s2ka
lgm_indx = (np.abs(time[:]-lgm_time)).argmin()
lgm_time = time[lgm_indx]
print lgm_indx, lgm_time*s2ka

# prepare figure
fig = mplt.figure(0, (120*mm2in, 240*mm2in))
ax  = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# bed topography and ice margin
im = iplt.bedtopoimage(nc, lgm_indx)
cs = iplt.icemargincontour(nc, lgm_indx, colors='white', alpha=0.5)

# velocity quiver
qv = iplt.surfvelquiver(nc, lgm_indx, width=0.0005) #, scale = 250
qv.set_rasterized(True)

# surface topography contours
cs = iplt.surftopocontour(nc, lgm_indx, levels=range(100, 6000, 100), linewidths=0.1)
cs = iplt.surftopocontour(nc, lgm_indx, levels=range(1000,6000,1000), linewidths=0.5)
cs.clabel(fontsize=6, fmt='%g')

# colorbars
#cax = fig.add_axes([20/800., 300/1600., 10/800., 200/1600.])
#cb = mplt.colorbar(im, cax=cax)
#cb.set_label('basal topography (m)')
#cax = fig.add_axes([60/800., 300/1600., 10/800., 200/1600.])
#cb = mplt.colorbar(qv, cax=cax)
#cb.set_label('ice surface velocity (m/a)')

# save
fig.savefig('lgmquiver.png', dpi=254)
