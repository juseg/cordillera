#!/usr/bin/env python2
# coding: utf-8

from hr_maps_base import icemaps

# plot
fig = icemaps(mis=4)

# save
print('saving...')
fig.savefig('hr_maps_mis4')
