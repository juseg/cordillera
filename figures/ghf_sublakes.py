#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

def open_gtif(filename):
    """Open GeoTIFF and return data and extent."""

    # open dataset
    ds = gdal.Open(filename)

    # read geotransform
    x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()
    assert dxdy == dydx == 0.0  # rotation parameters should be zero

    # compute image extent
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    x1 = x0 + dx*cols
    y1 = y0 + dy*rows

    # read image data
    data = ds.ReadAsArray()

    # close dataset and return image data and extent
    ds = None
    return data, (x0, x1, y0, y1)


# initialize figure
figw, figh = 160.0, 120.0
fig = plt.figure(figsize=(figw/25.4, figh/25.4))
ax = fig.add_axes([0, 0, 1, 1], projection=ut.pl.proj)
cax = fig.add_axes([1-70/figw, 10/figh, 60/figw, 5/figh])
ax.set_rasterization_zorder(2.5)

# plot topography
data, extent = open_gtif('../data/external/cded250k.tif')
ax.imshow(data, extent=extent, vmin=0e3, vmax=3e3, cmap='Greys')

# plot lake depths
data, extent = open_gtif('../data/processed/cordillera-narr-5km-'
                         'grip3222cool620+cgeo1+till1545+gou11simi-'
                         'sublakes-19100a.tif')
levs = [1, 3, 10, 31]
levs = [1, 2, 5, 10, 22, 46]
levs = [0.3, 1, 3, 10, 30]
cmap = plt.get_cmap('Blues', len(levs))
cols = cmap(range(len(levs)))
cs = ax.contourf(data, extent=extent, levels=levs, colors=cols,
                 extend='max', alpha=0.75)

# add colorbar
cb = fig.colorbar(cs, cax, orientation='horizontal', format='%g')
cb.set_label('subglacial lake depth (m)')

# set extents
ax.set_extent(extent, crs=ax.projection)

# save
ut.pl.savefig(fig)
