#!/usr/bin/env python2
# coding: utf-8

import os.path
import numpy as np
from paperglobals import *

offsets = np.arange(5.4, 6.8, 0.1)

# print table header
print '\n    dt ' + '| %7s ' * 6 % tuple(records),
print '\n  -----' + '+---------' * 6,

# for required temperature offset values
for i, dt in enumerate(offsets):
    print '\n   ' + '%3.1f' % dt,

    # for each record
    for j, rec in enumerate(records):
        this_run_path = run_path % (res, rec, round(dt*100))

        # if no file, print a blank line
        if not os.path.isfile(this_run_path + '-ts.nc'):
            print '|     -- ',

        # else print the MIS2 area
        else:

            # get MIS2 time
            idx, t = get_mis_times(this_run_path + '-ts.nc')
            idx, t = idx[-1], t[-1]
        
            # compute area from extra file
            nc = ncopen(this_run_path + '-extra.nc')
            thk = nc.variables['thk']
            time = nc.variables['time']
            idx = np.abs(time[:]*s2ka-t).argmin()
            iarea = (thk[idx] >= thkth).sum()*1e-4  # area at MIS2
            nc.close()

            # to compute true max area
            #iarea = (thk >= thkth).sum(axis=(1, 2)).max()*1e-4  # max area
            #iarea = (thk >= 8.0).any(axis=(0)).sum()*1e-4  # ice cover

            # print
            print '| %7.3f' % (iarea-2.0),

# print table footer
print '\n'
