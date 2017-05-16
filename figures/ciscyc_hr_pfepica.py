#!/usr/bin/env python2
# coding: utf-8

import util as ut

# parameters
res = '5km'
rec = ut.ciscyc_hr_records[1]
dt = ut.ciscyc_hr_offsets[1]
color = ut.ciscyc_hr_colours[1]

# plot
fig = ut.pl.fig_hr_pf(res, rec, dt, color)

# save
ut.pl.savefig(fig)
