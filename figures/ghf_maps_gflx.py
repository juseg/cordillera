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
            'grip3222cool620+{conf}+till1545{gflx}/y0005000.nc')
confargs = ['cgeo1+hynull'] + 5*['cgeo1']
gflxargs = 2*[''] + ['+dav13', '+gou11comb', '+gou11simi', '+sha04']

# initialize figure
figw, figh = 120.0, 130.0
fig, grid = iplt.subplots_mm(nrows=2, ncols=3, sharex=True, sharey=True,
                             figsize=(figw, figh),
                             left=2.5, right=20.0, bottom=2.5, top=2.5,
                             wspace=2.5, hspace=2.5)
cax = fig.add_axes([1-17.5/figw, 2.5/figh, 5.0/figw, 1-5.0/figh])

# loop on resolutions and heat flux maps
for i, (conf, gflx) in enumerate(zip(confargs, gflxargs)):
    ax = grid.flat[i]
    ax.set_rasterization_zorder(2.5)

    # open dataset
    filename = filepath.format(res='5km', conf=conf, gflx=gflx)
    print filename
    nc = iplt.load(filename)

    # plot
    # FIXME: including time argument here should give a better error message
    # FIXME: thickness threshold should not be necessary here?
    im = nc.imshow('bheatflx', ax, cmap='RdBu_r', vmin=20., vmax=120., thkth=-1)

    # close file and annotate
    nc.close()
    ax.text(0.9, 0.02, conf+gflx, ha='right', transform=ax.transAxes)

# add colorbar and save
cb = fig.colorbar(im, cax, extend='both')
cb.set_label(r'geothermal heat flux ($mW\,m^{-2}$)')
fig.savefig('ghf_maps_gflx')
