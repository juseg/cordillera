#!/usr/bin/env python2
# coding: utf-8

import os
import numpy as np
import zipfile
from netCDF4 import Dataset
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

# parameters
outdir = os.environ['HOME'] + '/pism/output/0.7.2/'
ghfmaps = ['gou11simi']
indexes = [1008]

# loop on geoflux maps
for ghf in ghfmaps:

    # file paths
    runname = 'cordillera-narr-5km/grip3222cool620+cgeo1+till1545+%s' % ghf
    ifilepath = outdir + runname + '/extra.nc'
    ofilelist = []
    prefix = 'processed/%s' % runname.replace('/', '-')

    # read extra output
    nc = Dataset(ifilepath)
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    conf = nc.variables['pism_config']
    rhoi = conf.ice_density
    rhow = conf.fresh_water_density

    # get grid size and origin
    cols = len(x)
    rows = len(y)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    x0 = x[0] - dx/2
    y0 = y[0] - dy/2
    x1 = x[-1] + dx/2
    y1 = y[-1] + dy/2

    # spatial reference system
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3978)

    # loop on model time
    for i in indexes:

        # read extra output
        age = -nc.variables['time'][i]/(365.0*24*60*60)
        h = nc.variables['thk'][i]
        t = nc.variables['temppabase'][i]

        # compute cold base areas
        warm = (h >= 1.0)*(t > -1e-6)

        # generate geotiff
        ofilepath = '%s-warmbase-%da.tif' % (prefix, age)
        driver = gdal.GetDriverByName('GTiff')
        rast = driver.Create(ofilepath, cols, rows, 1, gdal.GDT_Byte)
        rast.SetGeoTransform((x0, dx, 0, y1, 0, -dy))
        rast.SetProjection(srs.ExportToWkt())
        band = rast.GetRasterBand(1)
        band.WriteArray(np.flipud(warm.T))
        band.ComputeStatistics(0)
        band.FlushCache()

        # close datasets
        band = rast = None
        ofilelist.append(ofilepath)

    # create zip archive
    with zipfile.ZipFile(prefix + '-warmbase.zip', 'w') as zf:
        for f in ofilelist:
            zf.write(f, arcname=os.path.basename(f))

    # close extra output
    nc.close()
