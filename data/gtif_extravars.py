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
records = ['grip', 'epica']
offsets = [6.2, 5.9]
indexes = range(1039, 1100, 10)
variables = ['thk', 'topg', 'usurf', 'temppabase', 'velbase_mag']

# loop on records
for rec, dt in zip(records, offsets):

    # file paths
    runname = ('cordillera-narr-5km/%s3222cool%.0f+ccyc4+till1545'
               % (rec, dt*100))
    ifilepath = outdir + runname + '/extra.nc'
    ofilelist = []
    prefix = 'processed/%s' % runname.replace('/', '-')

    # read extra output
    nc = Dataset(ifilepath)
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]

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

    # loop on variables
    for varname in variables:

        # loop on model time
        for i in indexes:

            # read extra output
            age = -nc.variables['time'][i]/(365.0*24*60*60)
            z = nc.variables[varname][i]

            # generate geotiff
            ofilepath = '%s-%s-%da.tif' % (prefix, varname, age)
            driver = gdal.GetDriverByName('GTiff')
            rast = driver.Create(ofilepath, cols, rows, 1, gdal.GDT_Float32)
            rast.SetGeoTransform((x0, dx, 0, y1, 0, -dy))
            rast.SetProjection(srs.ExportToWkt())
            band = rast.GetRasterBand(1)
            band.WriteArray(np.flipud(z.T))
            band.ComputeStatistics(0)
            band.FlushCache()

            # close datasets
            band = rast = None
            ofilelist.append(ofilepath)

    # create zip archive
    with zipfile.ZipFile(prefix + '.zip', 'w') as zf:
        for f in ofilelist:
            zf.write(f, arcname=os.path.basename(f))

    # close extra output
    nc.close()
