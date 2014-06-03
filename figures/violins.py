#!/usr/bin/env python2
# coding: utf-8

from netCDF4 import Dataset
from matplotlib import pyplot as plt
from paperglobals import *
import seaborn as sns

# violin plot
sns.set_style("whitegrid")
fig, ax = plt.subplots()

# initialize time-series figure
#figw, figh = 85.0, 60.0
#fig = plt.figure(0, (figw*in2mm, figh*in2mm))
#ax = fig.add_axes([10/figw, 10/figh, 70/figw, 40/figh])

# read ice volume time series
data = []
for i, rec in enumerate(records):
    dt = offsets[i]
    nc = Dataset(run_path % ('10km', rec, dt*100) + '-ts.nc')
    slvol = nc.variables['slvol'][:]
    nc.close()
    data.append(slvol)

# plot
sns.violinplot(data, color=colors, names=labels, bw=1/12.0)

# set axes properties and save time series
print 'saving time series...'
ax.set_ylim(0.0, 10.0)
ax.set_ylabel('ice volume (m s.-l. eq.)')
fig.savefig('violins')
