#!/usr/bin/env python
# coding: utf-8

import os
import urllib
import numpy as np
from matplotlib import pyplot as plt

# data sources
urlbase = 'ftp://ftp.ncdc.noaa.gov/pub/data/paleo/'
urldict = {
    'epica': urlbase + 'icecore/antarctica/epica_domec/edc3deuttemp2007.txt',
    'lr04':  urlbase + 'contributions_by_author/lisiecki2005/lisiecki2005.txt'}

# additional sea-level data sources
# 'contributions_by_author/lea2002/lea2002.txt'
# 'contributions_by_author/siddall2003/siddall2003.txt'

# fetch data
for rec, url in urldict.iteritems():
    filename = 'data/%s.txt' % rec
    print filename
    if not os.path.isfile(filename):
        urllib.urlretrieve(url, filename)


# Initialize figure
figw, figh = 80.0, 60.0
fig, grid = plt.subplots(2, figsize=(figw/25.4, figh/25.4), sharex=True)
fig.subplots_adjust(left=10.0/figw, bottom=7.5/figh,
                    right=1-2.5/figw, top=1-2.5/figh,
                    hspace=1/((1+figh/2.5)/2-1))


# plot LR04 data (pick only the last 800 ka)
ax = grid[0]
age, d18o = np.genfromtxt('data/lr04.txt', skip_header=89, skip_footer=9387,
                          unpack=True, usecols=(0, 1))
ax.plot(age, d18o, '#1f78b4')  # alt. wiki color #0978ab

# set LR04 axes properties
ax.set_ylim(5.5, 2.5)
ax.set_yticks([3, 4, 5])
ax.set_ylabel(u'$\delta^{18}O$ (\u2030)')
ax.text(0.04, 0.85, '(a)', fontweight='bold', transform=ax.transAxes)

# plot EPICA data
ax = grid[1]
age, temp = np.genfromtxt('data/epica.txt', delimiter=(4, 13, 17, 13, 13),
                          skip_header=104, skip_footer=1,
                          unpack=True, usecols=(2, 4))
ax.plot(age/1000.0, temp, '#e31a1c')  # alt. wiki color #e0584e

# set EPICA axes properties
ax.set_yticks(range(-12, 6, 4))
ax.set_ylim(-12, 6)
ax.set_ylabel('$\Delta T$ (K)')
ax.set_xlim(800, 0)
ax.set_xlabel('age (ka)')
ax.text(0.04, 0.85, '(b)', fontweight='bold', transform=ax.transAxes)

# set common axes properties and add last glacial cycle box
for ax in grid:
    ax.grid(axis='y', c='0.5', ls='-', lw=0.1)
    ax.axvspan(111.0, 10.0, fc='0.95', lw=0.25)
    ax.yaxis.set_label_coords(-0.08, 0.5)

# save
fig.savefig('paleo-timeseries', dpi=254)
