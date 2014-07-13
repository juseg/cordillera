#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplot')

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from iceplot import plot as iplt

s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)

# file path
filename = '/home/julien/pism/output/cordillera-narr-6km-bl/' \
           'grip3222cool580+ccyc+till1545/y0120000-extra.nc'
tmin, tmax = -22.0, -8.0

# initialize figure
fig = plt.figure(0, (80/25.4, 160/25.4))
ax  = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# read extra output
print 'reading extra output...'
nc = Dataset(filename)
x = nc.variables['x']
y = nc.variables['y']
time = nc.variables['time']
mask = nc.variables['mask']
u = nc.variables['uvelbase']
v = nc.variables['vvelbase']
c = nc.variables['velbase_mag']

# compute last flow velocities
print 'computing last flow velocities...'
slidage = np.ones_like(mask[0])*-1.0
glaciated = np.zeros_like(mask[0])
lastu = np.zeros_like(u[0])
lastv = np.zeros_like(v[0])
imin, imax = [np.argmin(np.abs(time[:]*s2ka-t)) for t in (tmin, tmax)]
for i in range(imin, imax+1):
    print '[ %02.1f %% ]\r' % (100.0*(i-imin)/(imax-imin)),
    icy = (mask[i] == 2)
    sliding = icy * (c[i].data > 1.0)
    lastu = np.where(sliding, u[i], lastu)
    lastv = np.where(sliding, v[i], lastv)
    slidage = np.where(sliding, -time[i]*s2ka, slidage)
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
plotres=12  # in km

# plot last velocity stream lines
print 'plotting...'
ax.streamplot(x[:], y[:], lastu, lastv, color='k',
              density=(60.0/plotres, 120.0/plotres),
              cmap=cmap, norm=norm, linewidth=0.5)

# plot sliding age contours
cs = ax.contour(x[:], y[:], slidage, levels=range(10, 20, 1),
                colors='0.5', linewidths=0.25, dashes=(1, 3))
lx = np.arange(-1700, -1350, 75)*1e3
ly = np.ones_like(lx)*1100e3
cs.clabel(fontsize=6, fmt='%g',
          manual=np.vstack((lx,ly)).T)

# plot glaciated and non-sliding areas
ax.contourf(x[:], y[:], glaciated * (slidage < 0), levels=[0.5, 1.5],
            colors='none', hatches=['//'])
ax.contour(x[:], y[:], slidage, levels=[0.0],
           colors='k', linewidths=0.25)
ax.contour(x[:], y[:], glaciated, levels=[0.5],
           colors='k', linewidths=0.5)
nc.close()

# add colorbar and save
print 'saving...'
#cb = ColorbarBase(ax.cax, cmap=cmap, norm=norm, ticks=range(8, 23, 2))
#cb.set_label('Age of last basal sliding (kyr)')
fig.savefig('plot-lastflow')
