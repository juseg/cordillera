#!/usr/bin/env python
# coding: utf-8

import sys

sys.path.append('iceplot')

from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from iceplot import cm as icm
from paperglobals import *

in2mm = 1/25.4
pt2mm = 72*in2mm
bwu = 0.5  # base width unit
scale = '50m'

# Canadian Atlas Lambert projection
proj = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    secant_latitudes=(49.0, 77.0), globe=None, cutoff=0)

# Initialize figure
fig = plt.figure(0, (85/25.4, 60/25.4))
ax = fig.add_axes([0, 0, 1, 1], projection=proj)
ax.set_xlim((-3187.5e3, 3187.5e3))
ax.set_ylim((-0900e3, 3600e3))

# Draw ETOPO1 background and coastline
nc = Dataset('../data/etopo1.nc')
x = nc.variables['x']
y = nc.variables['y']
z = nc.variables['Band1']
w = (3*x[0]-x[1])/2
e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
n = (3*y[0]-y[1])/2
s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
im = ax.imshow(z, extent=(w, e, n, s),
               cmap=icm.topo, norm=Normalize(-6e3, 6e3))
cs = ax.contour(x[:], y[:], z[:], levels=[0],
                colors='#0978ab', linewidths=0.5*bwu, zorder=0.5)
nc.close()

# add lakes and rivers
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='rivers_lake_centerlines', scale=scale,
    edgecolor='#0978ab', facecolor='none', lw=1.0*bwu))
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='lakes', scale=scale,
    edgecolor='#0978ab', facecolor='#c6ecff', lw=0.5*bwu))

# add glaciers
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='physical', name='glaciated_areas', scale=scale,
#    edgecolor='#0978ab', facecolor='#f5f4f2', lw=1.0*bwu))

# add NaturalEarth coastlines
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='physical', name='coastline', scale=scale,
#    edgecolor='#0978ab', facecolor='none', lw=0.5*bwu))

# add country boundaries
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='cultural', name='admin_0_boundary_lines_land', scale=scale,
#    edgecolor='#646464', facecolor='none', lw=1.0*bwu))
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='cultural', name='admin_1_states_provinces_lines', scale=scale,
#    edgecolor='#646464', facecolor='none', lw=0.5*bwu))

# add Dyke 2005 deglacial outlines union
# available ages: 18.0, 17.5, 17.0, 16.5, 16.0, 15.5, 15.0, 14.5, 14.0,
#                 13.5, 13.0, 12.5, 12.0, 11.5, 11.0, 10.5, 10.25, 10.0
# calibrate ages: 21.4, 20.8, 20.2, 19.65, 19.1, 18.5, 17.9, 17.35, 16.8,
#                 16.2, 15.6, 14.8, 14.1, 13.45, 13.0, 12.7, 12.0, 11.45
raw_ages = [18.0, 17.0, 16.0, 15.0, 14.0]  #, 13.0, 12.0, 11.0, 10.0]
cal_ages = [21.4, 20.2, 19.1, 17.9, 16.8]  #, 15.6, 14.1, 13.0, 11.45]
union = None
for age in raw_ages:
    filename = '../data/ice%ik.shp' % age
    print 'reading %s ...' % filename
    for rec in shpreader.Reader(filename).records():
        if rec.attributes['SYMB'] == 'ICE':
            if union == None:
                union = rec.geometry
            else:
                union = union.union(rec.geometry)
ax.add_geometries(union, proj, edgecolor='none', facecolor='#f5f4f2', alpha=0.75)
ax.add_geometries(union, proj, edgecolor='#0978ab', facecolor='none', lw=0.5*bwu)

# add graticules
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='graticules_15', scale=scale,
    edgecolor='#000000', facecolor='none', lw=0.3*bwu))

# add modelling domain
ax.add_patch(plt.Rectangle((-2500e3, 0), 1500e3, 3000e3,
                           ec='k', fc='none', lw=2.0*bwu, zorder=10))

# save
fig.savefig('locmap')
