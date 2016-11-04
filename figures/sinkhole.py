#!/usr/bin/env python2

import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, Normalize

# matplotlib settings
plt.rc('image', origin='lower', interpolation='nearest')
plt.rc('font', size=8)


def extract(varname, r):
    """Return cropped array from selected variable"""
    i, j = 93, 110  # the problematic grid cell
    nc = Dataset('/home/julien/pism/output/cordillera-narr-5km-bl/'
                 'grip3222cool580+ccyc+till1545/y0120000-extra--0021700.000.nc')
    a = nc.variables[varname][0,i-r:i+1+r,j-r:j+1+r].T
    nc.close
    return a

# prepare figure
figw, figh = 8.0, 10.5
fig = plt.figure(0, (figw, figh))
ax = fig.add_axes([0.5/figw, 3.0/figh, 7.0/figw, 7.0/figh])

# plot velocity quiver
r = 40
mask = extract('mask', r)
topg = extract('topg', r)
usurf = extract('usurf', r)
u = extract('uvelsurf', r)
v = extract('vvelsurf', r)
u = np.sign(u)*np.log(1+np.abs(u)/100)
v = np.sign(v)*np.log(1+np.abs(v)/100)
c = (u**2 + v**2)**0.5
icy = (mask == 2)
usurf = np.ma.array(usurf, mask=(1-icy))
ax.imshow(topg-125.0, cmap='Greys')
ax.contour(usurf, levels=range(100, 5000, 100), colors='k', linewidths=0.2)
ax.contour(usurf, levels=range(1000, 5000, 1000), colors='k', linewidths=0.5)
ax.contourf(icy, levels=[0.5, 1.5], colors='w', alpha=0.75)
ax.contour(icy, levels=[0.5], colors='k')
ax.quiver(u, v, c, cmap='CMRmap_r')
ax.grid()
ax.set_title('velsurf')

# plot inset
for (k, varname) in enumerate(('topg', 'thk', 'usurf')):
    data = extract(varname, 2)
    ax = fig.add_axes([(0.5+2.5*k)/figw, 0.5/figh, 2.0/figw, 2.0/figh])
    ax.imshow(data, cmap='CMRmap_r')  #, norm=LogNorm())
    ax.grid()
    ax.set_title(varname)
    for (ii, jj), z in np.ndenumerate(data):
        if z > -1e6:
            ax.text(jj, ii, '%.1f' % z, ha='center', va='center',
                    bbox=dict(fc='white', lw=0.0, alpha=0.5))

# save
plt.savefig('sinkhole.png')
