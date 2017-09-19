#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np

# parameters
target = 2.1  # 1e6 km2

# initialize figure
fig, ax = ut.pl.subplots_ts()

# for each record
for i, rec in enumerate(ut.cisbed_records):
    c = ut.cisbed_colours[i]
    offsets = []
    fpareas = []

    # loop on offsets
    for dt in np.arange(5.5, 6.5, 0.05):

        # try to find max area
        try:

            # load extra file
            dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))
            nc = ut.io.load('output/e9d2d1f/cordillera-narr-10km/'
                            '%s+cisbed1+till1545/y???????-extra.nc' % dt_file)
            x = nc.variables['x'][:]
            y = nc.variables['y'][:]
            thk = nc.variables['thk'][909:1059]  # 29 to 14 ka
            mask = nc.variables['mask'][909:1059]  # 29 to 14 ka
            nc.close()

            # compute footprint area in 1e6 km2
            dx = x[1] - x[0]
            dy = y[1] - y[0]
            landprint = 1 - ((thk < 1.0) + (mask != 2)).prod(axis=0)
            a = landprint.sum()*dx*dy*1e-12

            # append to lists
            offsets.append(dt)
            fpareas.append(a)

        # else do nothing
        except (RuntimeError, IndexError):
            pass

    # continue if no files found
    if fpareas == []:
        continue

    # plot
    argmin = np.argmin(np.abs(np.array(fpareas)-target))
    ax.plot(offsets, fpareas, c=c, marker='o', label=rec)
    ax.plot(offsets[argmin], fpareas[argmin], c=c, marker='D')
    ax.axvline(offsets[argmin], lw=0.1, c=c)
    for dt, a in zip(offsets, fpareas):
        if a:
            ax.text(dt, a+5, '%.0f' % a, color=c, fontsize=4, ha='center',
                    clip_on=True)

# set axes properties
ax.axhline(target, lw=0.1, c='0.5')
ax.legend(loc='best')
ax.set_xlabel('temperature offset (K)')
ax.set_ylabel(r'glaciated area on land ($10^3\,km^2$)')

# save
ut.pl.savefig(fig)
