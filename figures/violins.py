#!/usr/bin/env python2
# coding: utf-8

from paperglobals import *

# violin plot
fig, ax = iplt.subplots()

# read ice volume time series
data = []
for i, rec in enumerate(records):
    dt = offsets[i]
    nc = open_ts_file('10km', rec, dt)
    slvol = nc.variables['slvol'][:]
    nc.close()
    data.append(slvol)

# plot
iplt.violinplot(data)

# set axes properties and save
print 'saving violins...'
ax.set_ylim(0.0, 10.0)
ax.set_ylabel('ice volume (m s.-l. eq.)')
fig.savefig('violins')
