#!/usr/bin/env python2
# coding: utf-8

import util as ut

# parameters
res = '5km'
rec = ut.lr.records[0]
dt = ut.lr.offsets[0]
color = ut.lr.colors[0]

# plot
fig = ut.pl.fig_hr_pf(res, rec, dt, color)

# save
print('saving...')
fig.savefig('hr_pf_grip')
