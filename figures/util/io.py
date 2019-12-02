# Copyright (c) 2014--2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Data input functions."""

import os
import numpy as np


def load(filepath):
    """Load file relative to PISM directory."""
    filepath = os.path.join(os.environ['HOME'], 'pism', filepath)
    return iplt.load(filepath)  # FIXME use xarray instead of iceplotlib


# unit conversion
a2s = 365.0 * 24 * 60 * 60
s2a = 1/a2s


# analysis functions
def bounded_argmin(a, coord, bmin, bmax):
    return np.ma.argmin(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def bounded_argmax(a, coord, bmin, bmax):
    return np.ma.argmax(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def get_mis_times(res, rec, dt, config='ccyc4+till1545'):
    """Return MIS indexes and times computed from output timeseries"""
    # FIXME: convert this to a function applied directly on the dt file.

    # load output time series
    nc = load('output/0.7.2-craypetsc/cordillera-narr-%s/'
              '%s3222cool%03d+%s/y???????-ts.nc'
              % (res, rec.replace(' ', '').lower(), round(100*dt), config))
    ts_time = nc.variables['time'][:]*s2a
    ts_ivol = nc.variables['ivol'][:]*1e-15
    nc.close()

    # locate snapshot times using time series
    mis = np.array([
        bounded_argmax(ts_ivol, ts_time, -80e3, -40e3),  # MIS4
        bounded_argmin(ts_ivol, ts_time, -60e3, -20e3),  # MIS3
        bounded_argmax(ts_ivol, ts_time, -40e3, -00e3)])  # MIS2

    # return indices and time values
    return mis, ts_time[mis]
