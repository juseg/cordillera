#!/usr/bin/env python2
# coding: utf-8

# FIXME: make iceplotlib a package
import sys
sys.path.append('iceplotlib')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

# velocity norm
norm = mcolors.LogNorm(1e4, 1e6)

# loop on resolutions and heat flux maps
for i, (conf, gflx) in enumerate(zip(confargs, gflxargs)):
    ax = grid.flat[i]
    ax.set_rasterization_zorder(2.5)

    # open dataset
    filename = filepath.format(res='5km', conf=conf, gflx=gflx)
    nc = iplt.load(filename)

    # try to plot water velocity
    try:
        x, y, u = nc._extract_xyz(r'bwatvel[0]', t)
        x, y, v = nc._extract_xyz(r'bwatvel[1]', t)
        w = (3*x[0]-x[1])/2
        e = (3*x[-1]-x[-2])/2
        n = (3*y[0]-y[1])/2
        s = (3*y[-1]-y[-2])/2
        c = (u**2 + v**2)**0.5
        print c.min(), c.mean(), c.max()
        im = ax.imshow(c, extent=(w, e, n, s), cmap='Blues', norm=norm)
        ax.contourf(x, y, c, levels=[-1e3, 1e3], colors='none', hatches=['//'])
        ax.contour(x, y, c, levels=[1e3], colors='k', linewidths=0.25)

    # else skip it
    except KeyError:
        x, y, c = nc._extract_xyz(r'thk', t)
        c = np.empty_like(c)

    # plot ice margin
    nc.icemargin(ax, t, thkth=1.0, linewidths=0.5)

    # close file and annotate
    nc.close()
    ax.text(0.9, 0.02, conf+gflx, ha='right', transform=ax.transAxes)

# add colorbar and save
cb = fig.colorbar(im, cax)
cb.set_label(r'subglacial water velocity ($m\,a^{-1}$)')
fig.savefig('ghf_maps_bwatvel')
