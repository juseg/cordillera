#!/usr/bin/env python2
# coding: utf-8

import util as ut

# parameters
res = '5km'
rec = ut.records[2]
dt = ut.offsets[2]
color = ut.colors[2]

# plot
fig = ut.pl.fig_hr_pf(res, rec, dt, color)

# save
print('saving...')
fig.savefig('hr_pf_epica')
