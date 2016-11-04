#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
from osgeo import gdal
from osgeo import osr

# parameters
res = '5km'
records = ut.hr.records
offsets = ut.hr.offsets

# loop on records
for i, rec in enumerate(records):
    filename = 'processed/deglacage-%s.tif' % rec

    # read extra output
    print 'reading %s extra output...' % rec
    nc = ut.io.open_extra_file(res, rec, offsets[i])
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    age = nc.variables['time'][:]*(-ut.s2ka)
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
    rast = driver.Create(filename, cols, rows, 1, gdal.GDT_Float32)
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
