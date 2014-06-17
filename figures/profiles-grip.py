#!/usr/bin/env python2
# coding: utf-8

from paperglobals import darkblue
from profiles import profiles

# parameters
res = '6km'
rec = 'grip'
dt = 5.8
color = darkblue

# plot
fig = profiles(res, rec, dt, color)

# save
print('saving...')
fig.savefig('profiles-grip')
