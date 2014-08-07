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
ll = ccrs.PlateCarree()
proj = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    secant_latitudes=(49.0, 77.0), globe=None, cutoff=0)

# ETOPO1 background topo
def draw_etopo1(**kwargs):
    """Draw ETOPO1 background and coastline"""
    nc = Dataset('data/etopo1.nc')
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

# Dyke 2004 LGM
def draw_lgm():
    """Draw LGM extent from Dyke deglacial outlines union"""
    # available ages: 18.0, 17.5, 17.0, 16.5, 16.0, 15.5, 15.0, 14.5, 14.0,
    #                 13.5, 13.0, 12.5, 12.0, 11.5, 11.0, 10.5, 10.25, 10.0
    # calibrate ages: 21.4, 20.8, 20.2, 19.65, 19.1, 18.5, 17.9, 17.35, 16.8,
    #                 16.2, 15.6, 14.8, 14.1, 13.45, 13.0, 12.7, 12.0, 11.45
    raw_ages = [18.0, 17.0, 16.0, 15.0, 14.0]  #, 13.0, 12.0, 11.0, 10.0]
    cal_ages = [21.4, 20.2, 19.1, 17.9, 16.8]  #, 15.6, 14.1, 13.0, 11.45]
    union = None
    for age in raw_ages:
        filename = 'data/ice%ik.shp' % age
        print 'reading %s ...' % filename
        for rec in shpreader.Reader(filename).records():
            if rec.attributes['SYMB'] == 'ICE':
                if union == None:
                    union = rec.geometry
                else:
                    union = union.union(rec.geometry)
    ax.add_geometries(union, proj, edgecolor='none', facecolor='#f5f4f2', alpha=0.75)
    ax.add_geometries(union, proj, edgecolor='#0978ab', facecolor='none', lw=1.0*bwu)

# Natural Earth elements
def draw_rivers():
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='rivers_lake_centerlines', scale=scale,
        edgecolor='#0978ab', facecolor='none', lw=1.0*bwu))

def draw_lakes():
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='lakes', scale=scale,
        edgecolor='#0978ab', facecolor='#c6ecff', lw=0.5*bwu))

def draw_glaciers():
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='glaciated_areas', scale=scale,
        edgecolor='#0978ab', facecolor='#f5f4f2', lw=1.0*bwu, alpha=0.75))

def draw_countries():
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='cultural', name='admin_0_boundary_lines_land', scale=scale,
        edgecolor='#646464', facecolor='none', lw=1.0*bwu))
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='cultural', name='admin_1_states_provinces_lines', scale=scale,
        edgecolor='#646464', facecolor='none', lw=0.5*bwu))

def draw_graticules():
    ax.add_feature(cfeature.NaturalEarthFeature(
        category='physical', name='graticules_15', scale=scale,
        edgecolor='#000000', facecolor='none', lw=0.25*bwu))

# Geographic names
def add_names():
    """Add geographic names"""

    # add names of palaeo-ice sheets
    txtkwa = dict(ha='center', va='center', transform=ll,
                  color='#0978AB', fontsize=8, style='italic')
    ax.text(-127, 55, 'CIS', **txtkwa)
    ax.text(-85, 60, 'LIS', **txtkwa)
    ax.text(-95, 77.5, 'IIS', **txtkwa)
    ax.text(-42, 74, 'GIS', **txtkwa)

    # add names of mountain ranges
    txtkwa = dict(ha='center', va='center', transform=ll,
                  color='k', fontsize=4, style='italic')
    ax.text(-146, 63.5, 'AR', **txtkwa)
    ax.text(-141, 61, 'WSEM', **txtkwa)
    ax.text(-129, 63, 'SMKM', **txtkwa)
    ax.text(-129, 57, 'SM', **txtkwa)
    ax.text(-128, 53, 'CM', **txtkwa)
    ax.text(-118, 52, 'CRM', **txtkwa)
    ax.text(-121, 49, 'NC', **txtkwa)

    # add names of intermontane plateaus
    ax.text(-127, 60, 'LL', **txtkwa)
    ax.text(-122, 52, 'IP', **txtkwa)
    ax.text(-122.5, 47.5, 'PL', **txtkwa)

# modelling domain
def draw_modeldomain():
    xmin = -2.5e6
    xmax = -1e6
    ymin = 0
    ymax = 3e6
    x = [xmin, xmin, xmax, xmax, xmin]
    y = [ymin, ymax, ymax, ymin, ymin]
    ax.plot(x, y, 'k', lw=bwu, transform=proj)

# Initialize figure
fig = plt.figure(0, (85/25.4, 60/25.4))
ax = fig.add_axes([0, 0, 1, 1], projection=proj)
ax.set_xlim((-3187.5e3, 3187.5e3))
ax.set_ylim((-0900e3, 3600e3))
ax.set_rasterization_zorder(2)

# draw stuff
draw_etopo1()
draw_rivers()
draw_lakes()
draw_lgm()
draw_modeldomain()
draw_graticules()
add_names()

# save
fig.savefig('locmap')
