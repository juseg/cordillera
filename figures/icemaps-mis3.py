#!/usr/bin/env python2
# coding: utf-8

from icemaps import icemaps

# plot
fig = icemaps(mis=3)

# save
print('saving...')
fig.savefig('icemaps-mis3')
