#!/usr/bin/env python2
# coding: utf-8

from paperglobals import *

# parameters
res = '5km'
records = records[0:3:2]
offsets = offsets[0:3:2]


# drawing function for animations
def draw(ax, idx):
    t = nc.variables['time'][idx]*s2ka
    print 'plotting %s at %s ka...' % (rec, t)
    ax.cla()

    # plot
    ax.imshow(nc, 'topg', idx, thkth=thkth,
              cmap=topo_cmap, norm=topo_norm)
    ax.icemargin(nc, idx, thkth=thkth,
                 linewidths=0.5)
    ax.contour(nc, 'usurf', idx, thkth=thkth,
               levels=range(200, 5000, 200),
               cmap=None, colors='k', linewidths=0.1)
    ax.contour(nc, 'usurf', idx, thkth=thkth,
               levels=range(1000, 5000, 1000),
               cmap=None, colors='k', linewidths=0.25)
    im = ax.imshow(nc, 'velsurf_mag', idx, thkth=thkth,
                   cmap=vel_cmap, norm=vel_norm, alpha=0.75)
    add_corner_tag(ax, '%s, %s ka' % (rec.upper(), -t))

    # return mappable for colorbar
    return im

# loop on records
for i, rec in enumerate(records):

    # load data
    nc = open_extra_file(res, rec, offsets[i])

    # initialize figure
    figw, figh = 70.0, 100.0
    fig, ax = iplt.subplots_mm(figsize=(figw, figh),
                               left=2.5, right=20.0, bottom=2.5, top=2.5,
                               wspace=2.5, hspace=2.5, projection='mapaxes')
    cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

    # draw first frame and colorbar
    im = draw(ax, 0)
    cb = fig.colorbar(im, cax, extend='both', format='%i',
                      ticks=np.logspace(1, 3.5, 6))
    cb.set_label(r'surface velocity ($m\,yr^{-1}$)', labelpad=-2.0)

    # save individual frames
    for idx in range(1200):
        draw(ax, idx)
        fig.savefig('frames/%s-%04i.png' % (rec, idx))

    # close nc file
    nc.close()
