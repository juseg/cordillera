#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# target area in 1e6 km2
target = 2.1

# initialize figure
fig, ax = iplt.subplots_mm(nrows=1, ncols=1, figsize=(85.0, 60.0),
                           left=10.0, right=2.5, bottom=10.0, top=2.5,
                           wspace=2.5, hspace=2.5)

# for each record
for i, rec in enumerate(ut.ciscyc_lr_records):
    c = ut.ciscyc_lr_colours[i]
    offsets = []
    misareas = []

    # for each temperature offset
    for dt in np.arange(5.7, 7.0, 0.05):

        # try to find MIS2 area
        try:

            # get MIS2 time
            t = ut.io.get_mis_times('10km', rec, dt)[1][2]

            # open extra file
            nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-10km/'
                            '%s3222cool%03d+ccyc4+till1545/y???????-extra.nc'
                            % (rec.replace(' ', '').lower(), round(100*dt)))
            time = nc.variables['time']
            idx = np.abs(time[:]-t*ut.a2s).argmin()
            thk = nc.variables['thk'][idx]
            mask = nc.variables['mask'][idx]
            nc.close()

            # compute grounded ice area at MIS 2
            a = ((thk >= ut.thkth)*(mask == 2)).sum()*1e-4
            offsets.append(dt)
            misareas.append(a)

        # else do nothing
        except RuntimeError:
            pass

    # plot
    argmin = np.argmin(np.abs(np.array(misareas)-target))
    ax.plot(offsets, misareas, c=c, marker='o')
    ax.plot(offsets[argmin], misareas[argmin], c=c, marker='D')
    ax.axvline(offsets[argmin], lw=0.1, c=c)
    for dt, a in zip(offsets, misareas):
        if a:
            ax.text(dt, a+0.02, '%.2f' % a, color=c, ha='center')

# set axes properties
ax.axhline(target, lw=0.1, c='0.5')
ax.set_xlim(5.7, 6.9)
ax.set_ylim(1.9, 2.4)
ax.set_xlabel('temperature offset (K)')
ax.set_ylabel(r'grounded ice extent at MIS 2 ($10^6\,km^2$)')

# save
ut.pl.savefig(fig)
