#!/usr/bin/env python2
# coding: utf-8

import util as ut
from profiles import profiles

# parameters
res = '5km'
rec = ut.records[2]
dt = ut.offsets[2]
color = ut.colors[2]

# plot
fig = profiles(res, rec, dt, color)

# save
print('saving...')
fig.savefig('profiles-epica')
