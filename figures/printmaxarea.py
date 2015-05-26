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

        # try to print MIS2 area
        try:
            # get MIS2 time
            idx, t = get_mis_times(res, rec, dt)
            idx, t = idx[-1], t[-1]
        
            # compute area from extra file
            nc = open_extra_file(res, rec, dt)
            thk = nc.variables['thk']
            time = nc.variables['time']
            idx = np.abs(time[:]*s2ka-t).argmin()
            iarea = (thk[idx] >= thkth).sum()*1e-4  # area at MIS2
            nc.close()

            # to compute true max area
            #iarea = (thk >= thkth).sum(axis=(1, 2)).max()*1e-4  # max area
            #iarea = (thk >= 8.0).any(axis=(0)).sum()*1e-4  # ice cover

            # print
            print '| %7.3f' % (iarea-2.1),

        # else print a blank cell
        except RuntimeError:
            print '|     -- ',

# print table footer
print '\n'
