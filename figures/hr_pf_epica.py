#!/usr/bin/env python2
# coding: utf-8

import util as ut

# parameters
res = '5km'
rec = ut.lr.records[2]
dt = ut.lr.offsets[2]
color = ut.lr.colors[2]

# plot
fig = ut.pl.fig_hr_pf(res, rec, dt, color)

# save
print('saving...')
fig.savefig('hr_pf_epica')
