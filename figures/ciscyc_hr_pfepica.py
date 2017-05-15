#!/usr/bin/env python2
# coding: utf-8

import util as ut

# parameters
res = '5km'
rec = ut.hr.records[1]
dt = ut.hr.offsets[1]
color = ut.hr.colors[1]

# plot
fig = ut.pl.fig_hr_pf(res, rec, dt, color)

# save
ut.pl.savefig(fig)
