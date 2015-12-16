#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# violin plot
fig, ax = iplt.subplots()
fig, ax = iplt.subplots_mm(1, 1, figsize=(85.0, 60.0),
                           left=10.0, bottom=10.0, right=2.5, top=2.5)

# read ice volume time series
data = []
for i, rec in enumerate(ut.records):
    dt = ut.offsets[i]
    nc = ut.io.open_ts_file('10km', rec, dt)
    slvol = nc.variables['slvol'][:]
    nc.close()
    data.append(slvol)

# plot
violins = iplt.violinplot(data)

# set colors
print violins
for p, c in zip(violins['bodies'], ut.colors):
    p.set_color(c)
violins['cbars'].set_color('0.5')
violins['cmins'].set_color('0.5')
violins['cmaxes'].set_color('0.5')

# set axes properties
ax.set_ylim(0.0, 10.0)
ax.set_ylabel('ice volume (m s.-l. eq.)')
ax.set_xlim(0.5, 6.5)
ax.set_xticks(np.arange(len(ut.records))+1)
ax.set_xticklabels(ut.labels)
ax.set_xlabel('record')

# save
print 'saving violins...'
fig.savefig('lr_violins')
