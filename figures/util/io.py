#!/usr/bin/env python2
# coding: utf-8

"""Data input functions."""

# FIXME: install iceplotlib as a package
import sys
sys.path.append('iceplotlib')

import os
import numpy as np
import iceplotlib.plot as iplt

# file path default params
pism_dir = os.environ['HOME'] + '/pism/'
config='ccyc4+till1545'
period='3222'
version = '0.7.2'

# unit conversion
a2s = 365.0 * 24 * 60 * 60
s2a = 1/a2s

# file open functions
def open_atm_file(res):
    return iplt.load(pism_dir + 'input/atm/cordillera-narr-%s.nc' % res)


def open_boot_file(res):
    return iplt.load(pism_dir + 'input/boot/cordillera-etopo1bed-%s.nc'
                     % res)


def open_dt_file(rec, dt, period='3222'):
    return iplt.load(pism_dir + 'input/dt/%s-%s-cool%i.nc'
                     % (rec, period, round(100*dt)))


def open_sd_file(res):
    return iplt.load(pism_dir + 'input/sd/cordillera-narr-%s.cr.nc' % res)


def open_ts_file(res, rec, dt,
                 config=config, period=period, version=version):
    return iplt.load(pism_dir + 'output/%s/cordillera-narr-%s/'
                     '%s%scool%i+%s/y0??0000-ts.nc'
                     % (version, res, rec, period, round(100*dt), config))


def open_extra_file(res, rec, dt,
                    config=config, period=period, version=version):
    return iplt.load(pism_dir + 'output/%s/cordillera-narr-%s/'
                     '%s%scool%i+%s/y0??0000-extra.nc'
                     % (version, res, rec, period, round(100*dt), config))


# analysis functions
def bounded_argmin(a, coord, bmin, bmax):
    return np.ma.argmin(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def bounded_argmax(a, coord, bmin, bmax):
    return np.ma.argmax(np.ma.array(a, mask=(coord < bmin)+(bmax < coord)))


def get_mis_times(res, rec, dt,
                  config=config, period=period, version=version):
    """Return MIS indexes and times computed from output timeseries"""

    # load output time series
    nc = open_ts_file(res, rec, dt,
                      config=config, period=period, version=version)
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

