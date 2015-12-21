#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

res = '10km'
offsets = np.arange(5.7, 7.0, 0.1)
target = 2.1

# prepare empty array
misareas = np.ma.masked_all((6, (len(offsets))))

# for required temperature offset values
for i, dt in enumerate(offsets):

    # for each record
    for j, rec in enumerate(ut.lr.records):

        # try to find MIS2 area
        try:

            # get MIS2 time
            t = ut.io.get_mis_times(res, rec, dt)[1][2]

            # open extra file
            print 'reading %s, %.1f' % (rec, dt)
            nc = ut.io.open_extra_file(res, rec, dt)
            time = nc.variables['time']
            idx = np.abs(time[:]-t*ut.a2s).argmin()
            thk = nc.variables['thk'][idx]
            mask = nc.variables['mask'][idx]

            # compute grounded ice area at MIS 2
            misareas[j, i] = ((thk >= ut.thkth)*(mask == 2)).sum()*1e-4

            # close
            nc.close()

        # else print a blank cell
        except RuntimeError:
            pass

# initialize figure
fig, ax = iplt.subplots_mm(nrows=1, ncols=1, figsize=(85.0, 60.0),
                           left=10.0, right=2.5, bottom=10.0, top=2.5,
                           wspace=2.5, hspace=2.5)

# plot
for i, rec in enumerate(ut.lr.records):
    c = ut.lr.colors[i]
    argmin = np.argmin(np.abs(misareas[i]-target))
    ax.plot(offsets, misareas[i], c=c, marker='o')
    ax.plot(offsets[argmin], misareas[i, argmin], c=c, marker='D')
    ax.axvline(offsets[argmin], lw=0.1, c=c)
    for dt, a in zip(offsets, misareas[i]):
        if a:
            ax.text(dt, a+0.02, '%.2f' % a, color=c, ha='center')

# set axes properties
ax.axhline(target, lw=0.1, c='0.5')
ax.set_xlim(5.7, 6.9)
ax.set_ylim(1.9, 2.4)
ax.set_xlabel('offset')
ax.set_ylabel('grounded ice area')

# save
print 'saving...'
fig.savefig('lr_misareas')
