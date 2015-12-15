#!/usr/bin/env python2
# coding: utf-8

from util import records, offsets, colors
from profiles import profiles

# parameters
res = '5km'
rec = records[0]
dt = offsets[0]
color = colors[0]

# plot
fig = profiles(res, rec, dt, color)

# save
print('saving...')
fig.savefig('profiles-grip')
