#!/usr/bin/env python
# coding: utf-8

from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature

in2mm = 1/25.4
pt2mm = 72*in2mm
bwu = 0.5  # base width unit
scale = '50m'

# Projection
proj = ccrs.NorthPolarStereo()

# Initialize figure
fig = plt.figure(0, (80/25.4, 80/25.4))
ax = fig.add_axes([0, 0, 1, 1], projection=proj)
ax.set_xlim(-6e6, 6e6)
ax.set_ylim(-6e6, 6e6)

# add NaturalEarth coastlines
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='coastline', scale=scale,
    edgecolor='k', facecolor='none', lw=0.5*bwu))

# add Ehlers & Gibbard 2003 LGM outline
# try to identify duplicates using centroids
centroids = []
shp = shpreader.Reader('data/lgm_global_simple.shp')
for i, geom in enumerate(shp.geometries()):
    x, y = geom.centroid.xy
    x, y = x[0], y[0]
    if y < 0:
        print 'record %i in southern hemisphere' % i
        continue
    if (x, y) in centroids:
        print 'record %i is a duplicate' % i
        continue
    else:
        print 'adding record %i with area %f ...' % (i, geom.area)
        centroids.append((x, y))
        ax.add_geometries(geom, ccrs.PlateCarree(), alpha=0.5,
                  edgecolor='none', facecolor='#0978ab', lw=bwu)

# add graticules
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='physical', name='graticules_15', scale=scale,
#    edgecolor='#000000', facecolor='none', lw=0.3*bwu))

# save
fig.savefig('paleo-glaciation', dpi=254)
