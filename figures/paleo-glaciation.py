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
proj = ccrs.Orthographic(central_longitude=-90.0, central_latitude=75.0)

# Initialize figure in inches
figw, figh = 80.0/25.4, 40.0/25.4
fig = plt.figure(0, (figw, figh))
fig.subplots_adjust(left=0.5/72/figw, bottom=0.5/72/figh,
                    right=1-0.5/72/figw, top=1-0.5/72/figh,
                    wspace=1/((1+figw/(1./72))/2-1))
grid = [fig.add_subplot(121+i, projection=proj) for i in range(2)]

# draw common parts
for ax in grid:
    ax.gridlines(color='0.5', linestyle='-', linewidth=0.1)
    ax.coastlines(edgecolor='k', lw=0.25)

# add present glaciers
grid[0].add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='glaciated_areas', scale=scale,
    edgecolor='none', facecolor='#0978ab', alpha=0.5,))

# add Ehlers & Gibbard 2003 LGM outline
# try to identify duplicates using centroids
centroids = []
shp = shpreader.Reader('data/lgm_simple.shp')
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
        grid[1].add_geometries(geom, ccrs.PlateCarree(),
                  edgecolor='none', facecolor='#0978ab', alpha=0.5)

# save
fig.savefig('paleo-glaciation')
