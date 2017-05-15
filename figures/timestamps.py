#!/usr/bin/env python2
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import netCDF4

# unit conversion
s2ka = 1/(365.0 * 24 * 60 * 60 * 1000)

# file paths
filepath = ('/home/juliens/pism/output/0.7.2-craypetsc/cordillera-narr-{res}/'
            'grip3222cool620+{conf}+till1545{gflx}/y???????-extra.nc')
hreslist = ['10km', '5km']
confargs = ['cgeo1+hynull'] + 5*['cgeo1']
gflxargs = 2*[''] + ['+dav13', '+gou11comb', '+gou11simi', '+sha04']

# initialize figure
fig, grid = plt.subplots(2, 1, sharex=True)

# loop on resolutions and heat flux maps
for ax, res in zip(grid, hreslist):
    for i, (conf, gflx) in enumerate(zip(confargs, gflxargs)):

        # read dataset
        filename = filepath.format(res=res, conf=conf, gflx=gflx)
        nc = netCDF4.MFDataset(filename)
        mtime = nc.variables['time'][:]*s2ka
        rtime = nc.variables['timestamp'][:]
        nc.close()
        #speed = np.gradient(mtime)/np.gradient(rtime)

        # plot
        ax.plot(mtime, rtime, label=conf+gflx)

    # add labels
    ax.text(0.95, 0.90, res, ha='right', transform=ax.transAxes)
    ax.set_ylabel('computing time (hours)')

# save
grid[0].legend(loc='best')
grid[1].set_xlabel('model time (ka)')
fig.savefig('timestamps')
