#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

res = '10km'
rec = 'grip'
offsets = np.arange(5.7, 7.0, 0.1)
target = 2.1

# prepare empty array
misareas = np.ma.masked_all((5, (len(offsets))))

# initialize figure
fig, ax = iplt.subplots_mm(nrows=1, ncols=1, figsize=(85.0, 60.0),
                           left=10.0, right=2.5, bottom=10.0, top=2.5,
                           wspace=2.5, hspace=2.5)

# for each configuration
for i, conf in enumerate(ut.sens.configs):
    c = ut.sens.colors[i]
    misareas = np.ma.masked_all_like(offsets)

    # for each temperature offset
    for j, dt in enumerate(offsets):

        # try to read MIS2 area
        try:

            # get MIS2 time
            t = ut.io.get_mis_times(res, rec, dt, config=conf)[1][2]

            # open extra file
            nc = ut.io.open_extra_file(res, rec, dt, config=conf)
            time = nc.variables['time']
            idx = np.abs(time[:]-t*ut.a2s).argmin()
            thk = nc.variables['thk'][idx]
            mask = nc.variables['mask'][idx]

            # compute grounded ice area at MIS 2
            a = ((thk >= ut.thkth)*(mask == 2)).sum()*1e-4
            print '%-30s, %.1f : %.2f, %.2f' % (conf, dt, t*1e-3, a)
            misareas[j] = a

            # close
            nc.close()

        # else do nothing
        except RuntimeError:
            pass

    # plot
    argmin = np.argmin(np.abs(misareas-target))
    ax.plot(offsets, misareas, c=c, marker='o')
    ax.plot(offsets[argmin], misareas[argmin], c=c, marker='D')
    ax.axvline(offsets[argmin], lw=0.1, c=c)
    for dt, a in zip(offsets, misareas):
        if a:
            ax.text(dt, a+0.02, '%.2f' % a, color=c, ha='center')

# set axes properties
ax.axhline(target, lw=0.1, c='0.5')
ax.set_xlim(5.7, 6.9)
ax.set_ylim(1.7, 2.4)
ax.set_xlabel('offset')
ax.set_ylabel('grounded ice area at MIS2')

# save
print 'saving...'
fig.savefig('sens_misareas')