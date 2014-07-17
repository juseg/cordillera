#!/usr/bin/env python2
# coding: utf-8

from paperglobals import darkred
from icemaps import icemaps

# plot
fig = icemaps(mis=2)

# save
print('saving...')
fig.savefig('icemaps-mis2')
