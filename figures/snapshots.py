#!/usr/bin/env python2
# coding: utf-8

from paperglobals import *
from matplotlib.ticker import FuncFormatter

# parameters
res = '10km'

# initialize snapshots figure
figw, figh = 120.0, 102.5
fig, grid = iplt.subplots(3, len(records), sharex=True, sharey=True,
                          figsize=(figw*in2mm, figh*in2mm),
                          subplot_kw={'projection': 'mapaxes'})
fig.subplots_adjust(left=5.0/figw, right=1-12.5/figw,
                    bottom=2.5/figh, top=1-5.0/figh,
                    hspace=1/((1+figh/2.5)/4-1))
cax = fig.add_axes([1-10.0/figw, 2.5/figh, 2.5/figw, 1-7.5/figh])

# loop on records[i]
for i, rec in enumerate(records):
    print 'reading %s extra output...' % rec

    # get MIS times
    mis_idces, mis_times = get_mis_times(res, rec, offsets[i])

    # load extra output
    nc = open_extra_file(res, rec, offsets[i])
    time = nc.variables['time'][:]*s2ka

    # round snapshot times to nearest slice
    mis_idces = [(np.abs(time[:]-t)).argmin() for t in mis_times]
    mis_times = time[mis_idces]

    # plot maps
    for j, t in enumerate(mis_idces):
        print 'plotting %s at %s...' % (rec, mis_times[j])
        ax = grid[j, i]
        ax.set_rasterization_zorder(2.5)
        ax.imshow(nc, 'topg', t, thkth=thkth,
                  cmap=topo_cmap, norm=topo_norm)
        ax.icemargin(nc, t, thkth=thkth,
                     linewidths=0.5)
        levs = range(0, 4001, 500)
        cs = ax.contourf(nc, 'usurf', t, thkth=thkth,
                         levels=levs, cmap='Blues_r',
                         norm=BoundaryNorm(levs, 256), alpha=0.75)
        ax.contour(nc, 'usurf', t, thkth=thkth,
                   levels=range(0, 4001, 500),
                   cmap=None, colors='k', linewidths=0.1)
        ax.contour(nc, 'usurf', t, thkth=thkth,
                   levels=range(1000, 5000, 1000),
                   cmap=None, colors='k', linewidths=0.25)
        add_corner_tag(ax, '%s ka' % (-mis_times[j]))

    # close extra file
    nc.close()

# add labels
for i, label in enumerate(labels):
    ax = grid[0, i]
    ax.text(0.5, 1.05, labels[i], ha='center',
            transform=ax.transAxes)
for j in range(3):
    ax = grid[j, 0]
    ax.text(-0.05, 0.5, 'MIS %i' % (4-j),
            ha='right', va='center', rotation='vertical',
            transform=ax.transAxes)

# mark location of the skeena mountains
add_pointer_tag(grid[1, 2], 'SM', xy=(-2000e3, 1450e3), xytext=(-1100e3, 1450e3))

# add colorbar and save
cb = fig.colorbar(cs, cax, ticks=levs[::2],
                  format=FuncFormatter(lambda x, pos: '%g' % (x/1000.0)))
cb.set_label(r'surface elevation (km)')  #, labelpad=-1.5*pt2mm)
print 'saving snapshots...'
fig.savefig('snapshots')
