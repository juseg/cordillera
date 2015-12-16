#!/usr/bin/env python2
# coding: utf-8

import util as ut
from profiles import profiles

# parameters
res = '5km'
rec = ut.records[0]
dt = ut.offsets[0]
color = ut.colors[0]

# plot
fig = profiles(res, rec, dt, color)

# save
print('saving...')
fig.savefig('profiles-grip')
