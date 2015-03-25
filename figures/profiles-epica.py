#!/usr/bin/env python2
# coding: utf-8

from paperglobals import records, offsets, colors
from profiles import profiles

# parameters
res = '5km'
rec = records[2]
dt = offsets[2]
color = colors[2]

# plot
fig = profiles(res, rec, dt, color)

# save
print('saving...')
fig.savefig('profiles-epica')
