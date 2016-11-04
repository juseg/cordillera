#!/usr/bin/env python2
# coding: utf-8

import os.path
import numpy as np
import util as ut
import iceplotlib.plot as iplt

res = '10km'
offsets = np.arange(5.7, 7.0, 0.1)

# print table header
print '\n    dt ' + '| %7s ' * 6 % tuple(ut.lr.records),
print '\n  -----' + '+---------' * 6,

# for required temperature offset values
for i, dt in enumerate(offsets):
    print '\n   ' + '%3.1f' % dt,

    # for each record
    for j, rec in enumerate(ut.lr.records):

        # try to print MIS2 area
        try:
            # get MIS2 time
            idx, t = ut.io.get_mis_times(res, rec, dt)
            idx, t = idx[-1], t[-1]

            # open extra file
            nc = ut.io.open_extra_file(res, rec, dt)
            thk = nc.variables['thk']
            mask = nc.variables['mask']
            time = nc.variables['time']
            idx = np.abs(time[:]-t*ut.a2s).argmin()

            # to compute maximum grounded ice area
            #iarea = ((thk[:] >= ut.thkth)*(mask[:] == 2)).sum(axis=(1, 2)).max()*1e-4

            # to compute grounded ice area at MIS 2
            iarea = ((thk[idx] >= ut.thkth)*(mask[idx] == 2)).sum()*1e-4

            # to compute area ever covered by grounded ice or footprint
            #iarea = ((thk[:] >= ut.thkth)*(mask[:] == 2)).any(axis=(0)).sum()*1e-4

            # print
            nc.close()
            print '| %7.3f' % (iarea-2.1),

        # else print a blank cell
        except RuntimeError:
            print '|     -- ',

# print table footer
print '\n'
