#!/usr/bin/env python2
# coding: utf-8

import util as ut

# initialize figure
fig, grid, cax = ut.pl.subplots_2_cax()

# loop on records
for i, rec in enumerate(ut.ciscyc_hr_records):
    dt = ut.ciscyc_hr_offsets[i]
    ax = grid[i]

    # get ice volume maximum
    t = ut.io.get_mis_times('5km', rec, dt)[-1][0]

    # load extra output
    nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-%s/'
                    '%s3222cool%03d+ccyc4+till1545/y0??0000-extra.nc'
                    % ('5km', rec.replace(' ', '').lower(), round(100*dt)))

    # plot
    im = nc.imshow('topg', ax, t, vmin=-3e3, vmax=6e3, cmap='Greys', zorder=-1)
    cs = nc.contour('topg', ax, t, levels=[0.0], colors='0.25',
                    linewidths=0.25, zorder=0)
    im = nc.imshow('velsurf_mag', ax, t, norm=ut.pl.velnorm, cmap='Blues',
                   alpha=0.75)
    cs = nc.contour('usurf', ax, t, levels=ut.pl.inlevs,
                    colors='0.25', linewidths=0.1)
    cs = nc.contour('usurf', ax, t, levels=ut.pl.utlevs,
                    colors='0.25', linewidths=0.25)
    cs = nc.icemargin(ax, t, colors='k', linewidths=0.25)

    # add map elements
    ut.pl.draw_natural_earth(ax)
    ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (rec.upper(), -t/1e3))

    # close extra file
    nc.close()

# add colorbar
cb = fig.colorbar(im, cax, extend='both', orientation='horizontal')
cb.set_label(r'surface velocity ($m\,a^{-1}$)')

# save
ut.pl.savefig(fig)
