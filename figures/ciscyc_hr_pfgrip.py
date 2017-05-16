#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np

# parameters
rec = ut.ciscyc_hr_records[0]
dt = ut.ciscyc_hr_offsets[0]
c = ut.ciscyc_hr_colours[0]
amax = 22.0
amin = 8.0
yplist = [1.7e6, 1.4e6, 1.1e6, 0.8e6]

# initialize figure
fig, grid = ut.pl.subplots_mm(len(yplist), figsize=(85.0, 95.0),
                              sharex=True, sharey=True,
                              left=10.0, bottom=10.0, right=2.5, top=2.5,
                              hspace=2.5)

# read extra output
nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                '%s3222cool%03d+ccyc4+till1545/y0??0000-extra.nc'
                % (rec.replace(' ', '').lower(), round(100*dt)))
age = -nc.variables['time'][:]/(1e3*365*24*60*60)
x = nc.variables['x'][:]
y = nc.variables['y'][:]

# compute age mask
agemask = (amin<age) * (age<amax)

# plot
for i, yp in enumerate(yplist):
    ax = grid[i]
    ax.set_rasterization_zorder(2.5)
    j = np.argmin(np.abs(y[:]-yp))
    mask = nc.variables['thk'][agemask, :, j] < ut.thkth
    topg = nc.variables['topg'][agemask, :, j]*1e-3
    surf = nc.variables['usurf'][agemask, :, j]*1e-3
    surf = np.where(mask, topg, surf)  # apply topg where ice-free
    mask = np.roll(mask, -1) * np.roll(mask, 1)  # shrink mask by 1 cell
    surf = np.ma.masked_where(mask, surf)  # apply mask
    ax.grid(axis='y')
    ax.plot(x*1e-3, surf.T, c=c, lw=0.1)
    ax.plot(x*1e-3, topg.T, c='k', lw=0.1)
    ax.text(0.04, 0.84, 'ABCD'[i], transform=ax.transAxes)

# close extra file
nc.close()

# set axes properties
grid[0].set_xlim(-2.35e3, -1.3e3)  # shared
grid[0].set_ylim(-1, 4)  # shared
grid[0].set_yticks(range(4))  # shared
grid[2].set_ylabel('elevation (km)')
grid[-1].set_xlabel('projection x-coordinate (km)')

# save
ut.pl.savefig(fig)
