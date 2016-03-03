#!/usr/bin/env python2
# coding: utf-8

import sys

sys.path.append('iceplotlib')

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from iceplotlib import cm as icm
from netCDF4 import Dataset

bwu = 0.5  # base width unit
scale = '50m'

# Geographic projections
ll = ccrs.PlateCarree()
cal = ccrs.LambertConformal(
    central_longitude=-95.0, central_latitude=49.0,
    false_easting=0.0, false_northing=0.0,
    standard_parallels=(49.0, 77.0), globe=None, cutoff=0)
proj = ccrs.LambertConformal(
    central_longitude=-135.0, central_latitude=45.0,
    false_easting=0.0, false_northing=0.0,
    standard_parallels=(45.0, 70.0), globe=None, cutoff=0)

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
    ax.add_geometries(union, cal, edgecolor='#b00000', facecolor='none', lw=1.0*bwu)

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
        category='physical', name='graticules_5', scale=scale,
        edgecolor='#000000', facecolor='none', lw=0.25*bwu))

# Geographic names
def add_names():
    """Add geographic names"""

    # add names of mountain ranges
    txtkwa = dict(ha='center', va='center', transform=ll, style='italic')
    ax.text(-149, 68.25, 'Brooks Range', rotation=0, **txtkwa)
    ax.text(-148, 63.25, 'Alaska Range', rotation=0, **txtkwa)
    ax.text(-143, 62, 'Wrangell\nMts', rotation=0, **txtkwa)
    ax.text(-140, 60.25, 'St Elias Mts', rotation=-15, **txtkwa)
    ax.text(-130, 63.75, 'McKenzie Mts', rotation=-30, **txtkwa)
    ax.text(-130, 62, 'Selwyn Mts', rotation=-30, **txtkwa)
    ax.text(-131, 60, 'Cassiar Mountains', rotation=-45, **txtkwa)
    ax.text(-119, 51.5, 'Columbia Mts', rotation=-30, **txtkwa)
    ax.text(-120, 54, 'Rocky Mountains', rotation=-30, **txtkwa)
    ax.text(-128, 54, 'Coast Mountains', rotation=-45, **txtkwa)
    ax.text(-128, 56, 'Skeena Mts', rotation=-45, **txtkwa)
    ax.text(-121, 48, 'N. Cascades', rotation=90, **txtkwa)

    # add names of intermontane plateaus
    ax.text(-127, 60, 'Liard\nLowland', **txtkwa)
    ax.text(-122.5, 52, 'Interior\nPlateau', **txtkwa)
    #ax.text(-124, 54, 'Fraser\nPlateau', **txtkwa)
    #ax.text(-123, 48, 'Puget\nLowland', **txtkwa)

    # mark Puget Lowland. annotate is tricky
    xy = ax.projection.transform_point(-122, 48, src_crs=ll)
    xytext = ax.projection.transform_point(-126, 46, src_crs=ll)
    ax.annotate('Puget\nLowland', xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle='->'), **txtkwa)

    # add names of islands
    ax.text(-132, 53, 'Q. Charlotte I.', rotation=-45, **txtkwa)
    ax.text(-126, 49.5, 'Vancouver Island', rotation=-30, **txtkwa)

    # add other names
    txtkwa = dict(ha='center', va='center', transform=ll,
                  fontsize=10, style='italic')
    ax.text(-135, 71, 'ARCTIC OCEAN', color='#0978AB', **txtkwa)
    ax.text(-145, 50, 'PACIFIC\n\nOCEAN', color='#0978AB', **txtkwa)
    ax.text(-110, 60, 'CANADIAN\n\nPRAIRIES', **txtkwa)

# modelling domain
def draw_modeldomain():
    xmin = -2.5e6
    xmax = -1e6
    ymin = 0
    ymax = 3e6
    x = [xmin, xmin, xmax, xmax, xmin]
    y = [ymin, ymax, ymax, ymin, ymin]
    ax.plot(x, y, 'k', lw=2*bwu, transform=cal)

# initialize figure
fig = plt.figure(0, (135/25.4, 100/25.4))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection=proj)
ax.set_xlim((-2025e3, 2025e3))
ax.set_ylim((-0e3, 3000e3))
ax.set_rasterization_zorder(2)

# draw stuff
draw_etopo1()
draw_rivers()
draw_lakes()
draw_glaciers()
draw_lgm()
draw_modeldomain()
draw_graticules()
add_names()

# save
fig.savefig('locmap')
