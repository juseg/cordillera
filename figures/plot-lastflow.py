#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplotlib')

import os
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
from iceplotlib import plot as iplt
from iceplotlib.colors import default_cmaps, default_norms

s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)

# file path
filename = (os.environ['HOME'] + '/pism/output/0.7.2-craypetsc/cordillera-narr-5km/'
            'grip3222cool620+ccyc4+till1545/y???????-extra.nc')

# index bounds
imin, imax = 75, 150
jmin, jmax = 100, 175
kmin, kmax = 899, 1120

# initialize figure
figw, figh = 85.0, 60.0
fig, ax = iplt.subplots_mm(figsize=(figw, figh),
                           left=2.5, right=20.0, bottom=2.5, top=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])
ax.axis('off')

# read extra output
print 'reading extra output...'
nc = iplt.load(filename)
x = nc.variables['x'][imin:imax]
y = nc.variables['y'][jmin:jmax]
time = nc.variables['time'][kmin:kmax]*s2ka
mask = nc.variables['mask'][kmin:kmax, imin:imax, jmin:jmax]
topg = nc.variables['topg'][0, imin:imax, jmin:jmax]
u = nc.variables['uvelbase'][kmin:kmax, imin:imax, jmin:jmax]
v = nc.variables['vvelbase'][kmin:kmax, imin:imax, jmin:jmax]
c = nc.variables['velbase_mag'][kmin:kmax, imin:imax, jmin:jmax]
nc.close()

# coordinate bounds
w = (3*x[0]-x[1])/2
e = (3*x[-1]-x[-2])/2
s = (3*y[0]-y[1])/2
n = (3*y[-1]-y[-2])/2
tmin, tmax = time[[0, -1]]
print 'WE bounds:', w, e
print 'NS bounds:', n, s
print 'time bounds:', tmin, tmax

# compute last flow velocities
print 'computing last flow velocities...'
slidage = np.ones_like(mask[0])*-1.0
glaciated = np.zeros_like(mask[0])
lastu = np.zeros_like(u[0])
lastv = np.zeros_like(v[0])
for k, t in enumerate(time):
    icy = (mask[k] == 2)
    sliding = icy * (c[k].data > 1.0)
    lastu = np.where(sliding, u[k], lastu)
    lastv = np.where(sliding, v[k], lastv)
    slidage = np.where(sliding, -time[k], slidage)
    glaciated = np.where(icy, 1, glaciated)

# transpose and scale last flow velocity
lastu = np.ma.masked_where(slidage < 0, lastu).T
lastv = np.ma.masked_where(slidage < 0, lastv).T
lastc = (lastu**2 + lastv**2)**0.5
slidage = slidage.T
glaciated = glaciated.T

# plot parameters
cmap='RdBu_r'
norm=Normalize(-tmax, -tmin)
plotres=6e3  # in m
density=((e-w)/25/plotres, (n-s)/25/plotres)

# plot bedrock topography
ax.imshow(topg.T, extent=(w, e, s, n),
          cmap=default_cmaps['topg'], norm=default_norms['topg'])
# plot last velocity stream lines
print 'plotting stream lines...'
ax.streamplot(x[:], y[:], lastu, lastv, color=slidage,
              density=density, cmap=cmap, norm=norm, linewidth=0.5)

# plot sliding age contour
cs = ax.contour(x[:], y[:], slidage, levels=[25.0],
                colors='k', linewidths=0.25, dashes=(1, 3))

# plot glaciated and non-sliding areas
ax.contourf(x[:], y[:], glaciated * (slidage < 0), levels=[0.5, 1.5],
            colors='none', hatches=['//'])
ax.contour(x[:], y[:], slidage, levels=[0.0],
           colors='k', linewidths=0.25)
ax.contour(x[:], y[:], glaciated, levels=[0.5],
           colors='k', linewidths=0.5)

# add colorbar and save
print 'saving...'
cb = ColorbarBase(cax, cmap=cmap, norm=norm) #, ticks=range(8, 23, 2))
cb.set_label('Age of last basal sliding (kyr)')
ax.set_xlim(w, e)
ax.set_ylim(s, n)
fig.savefig('plot-lastflow')
