#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np

# parameters
target = 2.25  # 1e6 km2

# initialize figure
fig, grid, cax = ut.pl.subplots_2_cax()

# for each record
for i, rec in enumerate(ut.cisbed_records):
    ax = grid[i]
    c = ut.cisbed_colours[i]
    dt = ut.cisbed_offsets[i]
    dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))
    run_dir = 'output/e9d2d1f/cordillera-narr-10km/%s+cisbed1+till1545' % dt_file

    # load extra file
    nc = ut.io.load(run_dir + '/y???????-extra.nc')
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    thk = nc.variables['thk'][909:1059]  # 29 to 14 ka
    mask = nc.variables['mask'][909:1059]  # 29 to 14 ka

    # compute footprint
    landprint = 1 - ((thk < 1.0) + (mask != 2)).prod(axis=0)

    # plot
    im = nc.imshow('topg', ax, 0.0, vmin=0.0, vmax=3e3, cmap='Greys', zorder=-1)
    cs = nc.contour('topg', ax, 0.0, levels=[0.0], colors='0.25',
                    linewidths=0.25, zorder=0)
    cs = ax.contourf(x, y, landprint, levels=[0.5, 1.5], colors=[c], alpha=0.75)

    # close extra file
    nc.close()

    # add map elements
    ut.pl.draw_lgm_outline(ax, c='k')
    ut.pl.draw_natural_earth(ax)
    ut.pl.add_corner_tag(ax, rec)

# add colorbar
cb = fig.colorbar(im, cax, extend='both', orientation='horizontal')
cb.set_label(r'bedrock altitude (m)')

# save
ut.pl.savefig(fig)
