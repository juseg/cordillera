#!/usr/bin/env python2
# coding: utf-8

import util as ut

# plot
fig = ut.pl.fig_hr_maps_mis(mis=3)

# save
print('saving...')
fig.savefig('hr_maps_mis3')
