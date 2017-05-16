#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# violin plot
fig, ax = iplt.subplots_mm(nrows=1, ncols=1, figsize=(85.0, 60.0),
                           left=10.0, bottom=10.0, right=2.5, top=2.5)

# read ice volume time series
data = []
for i, rec in enumerate(ut.ciscyc_lr_records):
    dt = ut.ciscyc_lr_offsets[i]
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-10km/'
                    '%s3222cool%03d+ccyc4+till1545/y???????-ts.nc'
                    % (rec.replace(' ', '').lower(), round(100*dt)))
    slvol = nc.variables['slvol'][:]
    nc.close()
    data.append(slvol)

# plot
violins = iplt.violinplot(data)

# set colors
for p, c in zip(violins['bodies'], ut.ciscyc_lr_colours):
    p.set_color(c)
violins['cbars'].set_color('0.5')
violins['cmins'].set_color('0.5')
violins['cmaxes'].set_color('0.5')

# set axes properties
ax.set_ylim(0.0, 10.0)
ax.set_ylabel('ice volume (m s.-l. eq.)')
ax.set_xlim(0.5, 6.5)
ax.set_xticks(np.arange(6)+1)
ax.set_xticklabels(ut.ciscyc_lr_records)
ax.set_xlabel('record')

# save
ut.pl.savefig(fig)
