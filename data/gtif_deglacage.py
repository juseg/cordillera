#!/usr/bin/env python2
# coding: utf-8

import os
import numpy as np
from netCDF4 import MFDataset
from osgeo import gdal
from osgeo import osr

# parameters
pismdir = os.environ['HOME'] + '/pism/'
records = ['grip', 'epica']
offsets = [6.2, 5.9]

# make output directory if missing
if not os.path.exists('processed'):
    os.makedirs('processed')

# loop on records
for rec, dt in zip(records, offsets):
    ifilename = (pismdir + 'output/0.7.2/cordillera-narr-5km/'
                 '%s3222cool%i+ccyc4+till1545/y0??0000-extra.nc'
                 % (rec, round(100*dt)))
    ofilename = 'processed/deglacage-%s.tif' % rec

    # read extra output
    print 'processing %s extra output...' % rec
    nc = MFDataset(ifilename)
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    age = -nc.variables['time'][:]/(1e3*365.0*24*60*60)
    thk = nc.variables['thk'][:]
    nc.close()

    # get grid size and origin
    cols = len(x)
    rows = len(y)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    x0 = x[0] - dx/2
    y0 = y[0] - dy/2
    y1 = y[-1] + dy/2

    # compute deglaciation age
    icy = (thk >= 1.0)
    nlastfree = icy[::-1].argmax(axis=0)  # number of last free timesteps
    deglacage = (age[-nlastfree-1]+age[-nlastfree]) / 2

    # fill in always and never icy cases
    nevericy = (nlastfree == 0)*(icy[-1] == 0)
    alwaysicy = (nlastfree == 0)*(icy[-1] == 1)
    deglacage[alwaysicy] = age[-1]
    deglacage[nevericy] = age[0]

    # create geotiff
    driver = gdal.GetDriverByName('GTiff')
    rast = driver.Create(ofilename, cols, rows, 1, gdal.GDT_Float32)
    rast.SetGeoTransform((x0, dx, 0, y1, 0, -dy))
    band = rast.GetRasterBand(1)
    band.WriteArray(np.flipud(deglacage.T))

    # inform SRS
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3978)
    rast.SetProjection(srs.ExportToWkt())
    band.FlushCache()
    gtif = rast = None

    # compute contours
    #driver = ogr.GetDriverByName('ESRI Shapefile')
    #shp = driver.CreateDataSource('test')
    #lyr = shp.CreateLayer('contour')
    #field_defn = ogr.FieldDefn('ID', ogr.OFTInteger)
    #lyr.CreateField(field_defn)
    #field_defn = ogr.FieldDefn('elev', ogr.OFTReal)
    #lyr.CreateField(field_defn)
    #gdal.ContourGenerate(band, 10, 0, [], 0, 0, lyr, 0, 1)
    #lyr = None
    #shp = None
