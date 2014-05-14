#!/usr/bin/env python
# coding: utf-8

from matplotlib import pyplot as mplt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature

in2mm = 1/25.4
pt2mm = 72*in2mm
bwu = 0.1*pt2mm  # base width unit
scale = '50m'

# Canadian Atlas Lambert projection
proj = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    secant_latitudes=(49.0, 77.0), globe=None, cutoff=0)

# Initialize figure
fig = mplt.figure(0, (80/25.4, 60/25.4))
ax = fig.add_axes([0, 0, 1, 1], projection=proj)
ax.set_xlim((-3600e3, 2800e3))
ax.set_ylim((-1200e3, 3600e3))

# draw simple background map
#ax.stock_img()

# add lakes and rivers
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='rivers_lake_centerlines', scale=scale,
    edgecolor='#0978ab', facecolor='none', lw=1.0*bwu))
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='lakes', scale=scale,
    edgecolor='#0978ab', facecolor='#c6ecff', lw=0.5*bwu))
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='physical', name='glaciated_areas', scale=scale,
#    edgecolor='#0978ab', facecolor='#f5f4f2', lw=1.0*bwu))

# add coastlines
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='coastline', scale=scale,
    edgecolor='#0978ab', facecolor='none', lw=0.5*bwu))
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='physical', name='land', scale=scale,
#    edgecolor='#0978ab', facecolor='#fefee9', lw=0.5*bwu))

# add country boundaries
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='cultural', name='admin_0_boundary_lines_land', scale=scale,
#    edgecolor='#646464', facecolor='none', lw=5.0*bwu, linestyle='-.'))
#ax.add_feature(cfeature.NaturalEarthFeature(
#    category='cultural', name='admin_1_states_provinces_lines', scale=scale,
#    edgecolor='#0978ab', facecolor='#f5f4f2', lw=1.0*bwu))

# add Dyke 2005 16.8 ka deglaciation outline
for rec in shpreader.Reader('../data/ice145k.shp').records():
    if rec.attributes['SYMB'] == 'ICE':
        ax.add_geometries(rec.geometry, proj,
                          edgecolor='#b00000', facecolor='none', lw=2.0*bwu)

# add graticules
ax.add_feature(cfeature.NaturalEarthFeature(
    category='physical', name='graticules_15', scale=scale,
    edgecolor='#000000', facecolor='none', lw=0.3*bwu))

# add modelling domain
rect = mplt.Rectangle((-2500e3, 0), 1500e3, 3000e3,
                      ec='k', fc='none', lw=2.0*bwu, zorder=10)
ax.add_patch(rect)

fig.savefig('cordillera-cycle-locmap')
