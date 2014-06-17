#!/usr/bin/env python2
# coding: utf-8

from paperglobals import darkred
from profiles import profiles

# parameters
res = '6km'
rec = 'epica'
dt = 5.6
color = darkred

# plot
fig = profiles(res, rec, dt, color)

# save
print('saving...')
fig.savefig('profiles-epica')
