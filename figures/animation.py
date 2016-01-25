#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt

# parameters
res = '5km'
records = ut.hr.records
offsets = ut.hr.offsets


# drawing function for animations
def draw(ax1, ax2, t):
    print 'plotting %s at %.1f ka...' % (rec, -t/1e3)
    ax1.cla()
    ax2.cla()
    ax2.background_patch.set_visible(False)

    # plot
    nc.imshow('topg', ax=ax1, t=t,
              cmap=ut.topo_cmap, norm=ut.topo_norm, zorder=-1)
    ut.pl.draw_ne_vectors(ax2)
    nc.contour('topg', ax=ax2, t=t, levels=[0.0], cmap=None,
               colors='0.25', linewidths=0.25, zorder=0)
    nc.icemargin(ax=ax2, t=t, linewidths=0.5)
    nc.contour('usurf', ax=ax2, t=t,
               levels=range(200, 5000, 200),
               cmap=None, colors='k', linewidths=0.1)
    nc.contour('usurf', ax=ax2, t=t,
               levels=range(1000, 5000, 1000),
               cmap=None, colors='k', linewidths=0.25)
    im = nc.imshow('velsurf_mag', ax=ax2, t=t,
                   cmap=ut.vel_cmap, norm=ut.vel_norm, alpha=0.75)
    ut.pl.add_corner_tag(ax2, '%s, %.1f ka' % (rec.upper(), -t/1e3))

    # return mappable for colorbar
    return im

# loop on records
for i, rec in enumerate(records):

    # load data
    nc = ut.io.open_extra_file(res, rec, offsets[i])
    time = nc.variables['time'][:]*ut.s2a

    # initialize figure
    figw, figh = 70.0, 100.0
    fig, ax1 = iplt.subplots_mm(figsize=(figw, figh), projection=ut.pl.proj,
                               left=2.5, right=20.0, bottom=2.5, top=2.5,
                               wspace=2.5, hspace=2.5)
    ax1.set_rasterization_zorder(2.5)
    nc.imshow('topg', ax=ax1, t=time[0],
              cmap=ut.topo_cmap, norm=ut.topo_norm, zorder=-1)
    ax2 = ut.pl.make_geoaxes(ax1)  # only one image per geoaxes
    cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

    # draw first frame and colorbar
    im = draw(ax1, ax2, time[0])
    cb = fig.colorbar(im, cax, extend='both', format='%i',
                      ticks=np.logspace(1, 3.5, 6))
    cb.set_label(r'surface velocity ($m\,a^{-1}$)', labelpad=-2.0)

    # save individual frames
    for i, t in enumerate(time):
        draw(ax1, ax2, t)
        fig.savefig('frames/%s-%04i.png' % (rec, i))

    # close nc file
    nc.close()
