#!/usr/bin/env python
# coding: utf-8

from netCDF4 import Dataset
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature

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
fig = plt.figure(0, (170/25.4, 100/25.4))
ax = fig.add_axes([0, 0, 1, 1], projection=proj)
ax.set_xlim((-4250e3, 4250e3))
ax.set_ylim((-1200e3, 3800e3))

# Draw ETOPO1 background and coastline
#nc = Dataset('../data/etopo1.nc')
#x = nc.variables['x']
#y = nc.variables['y']
#z = nc.variables['Band1']
#w = (3*x[0]-x[1])/2
#e = (3*x[-1]-x[-2])/2 - (x[-1]-x[-2])/2  # weird but works
#n = (3*y[0]-y[1])/2
#s = (3*y[-1]-y[-2])/2 - (y[-1]-y[-2])/2  # weird but works
#im = ax.imshow(z, extent=(w, e, n, s),
#               cmap=icm.topo, norm=Normalize(-6e3, 6e3))
#cs = ax.contour(x[:], y[:], z[:], levels=[0],
#                colors='#0978ab', linewidths=0.5*bwu, zorder=0.5)
#nc.close()

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
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='coastline', scale=scale,
    edgecolor='#0978ab', facecolor='none', lw=0.5*bwu))

# add country boundaries
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='cultural', name='admin_0_boundary_lines_land', scale=scale,
#    edgecolor='#646464', facecolor='none', lw=1.0*bwu))
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='cultural', name='admin_1_states_provinces_lines', scale=scale,
#    edgecolor='#646464', facecolor='none', lw=0.5*bwu))

# add graticules
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='graticules_15', scale=scale,
    edgecolor='#000000', facecolor='none', lw=0.3*bwu))

# add modelling domain
ax.add_patch(plt.Rectangle((-2500e3, 0), 1500e3, 3000e3,
                           ec='k', fc='none', lw=2.0*bwu, zorder=10))

# save
fig.savefig('map-northamerica')
