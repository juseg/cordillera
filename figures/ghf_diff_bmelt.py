#!/usr/bin/env python2
# coding: utf-8

# FIXME: make iceplotlib a package
import sys
sys.path.append('iceplotlib')

import numpy as np
import matplotlib.pyplot as plt
import iceplotlib.plot as iplt

# time for plot in years
t = -19000.0

# file paths
filepath = ('/home/juliens/pism/output/0.7.2/cordillera-narr-{res}/'
            'grip3222cool620+{conf}+till1545{gflx}/y???????-extra.nc')
confargs = ['cgeo1+hynull'] + 5*['cgeo1']
gflxargs = 2*[''] + ['+dav13', '+gou11comb', '+gou11simi', '+sha04']

# initialize figure
figw, figh = 120.0, 130.0
fig, grid = iplt.subplots_mm(nrows=2, ncols=3, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# open reference dataset
filename = filepath.format(res='5km', conf='cgeo1', gflx='')
nc = iplt.load(filename)
xref, yref, zref = nc._extract_xyz('bmelt', t=t)
nc.close()

# loop on resolutions and heat flux maps
for i, (conf, gflx) in enumerate(zip(confargs, gflxargs)):
    ax = grid.flat[i]
    ax.set_aspect(1.0)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_rasterization_zorder(2.5)

    # open dataset
    filename = filepath.format(res='5km', conf=conf, gflx=gflx)
    nc = iplt.load(filename)
    x, y, z = nc._extract_xyz('bmelt', t=t)
    w = (3*x[0]-x[1])/2
    e = (3*x[-1]-x[-2])/2
    n = (3*y[0]-y[1])/2
    s = (3*y[-1]-y[-2])/2

    # plot
    diff = z-zref
    im = ax.imshow(diff, extent=(w, e, n, s), cmap='RdBu_r', vmin=-0.05, vmax=0.05)
    ax.contourf(x, y, diff, levels=[-1e-6, 1e-6], colors='none', hatches=['//'])
    ax.contour(x, y, diff, levels=[-1e-6, 1e-6], colors='k', linewidths=0.25)
    nc.icemargin(ax, t, thkth=1.0, linewidths=0.5)

    # close file and annotate
    nc.close()
    ax.text(0.9, 0.02, conf+gflx, ha='right', transform=ax.transAxes)

# add colorbar and save
cb = fig.colorbar(im, cax)
cb.set_label(r'basal melt rate anomaly ($m\,a^{-1}$)')
fig.savefig('ghf_diff_bmelt')
