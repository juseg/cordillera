#!/usr/bin/env python2
# coding: utf-8

import util as ut

# plot
fig = ut.pl.fig_hr_maps_mis(mis=2)

# save
print('saving...')
ut.pl.savefig(fig)
