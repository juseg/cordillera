#!/usr/bin/env python2
# coding: utf-8

"""Utils and parameters for this project."""


from matplotlib.colors import LogNorm, Normalize
import io
import pl

# unit conversion
# FIXME: use iplt.subplots_mm instead
in2mm = 1/25.4
pt2mm = 72*in2mm
a2s = 365.0 * 24 * 60 * 60
s2a = 1/a2s
s2ka = s2a/1e3

# default params
res = '10km'
dt = 5.8
rec = 'grip'

# colors
topo_cmap = 'Greys'
topo_norm = Normalize(-3000, 6000)
vel_cmap = 'RdBu_r'
vel_norm = LogNorm(1e1, 1e3)

# record properties
records = ['grip', 'ngrip', 'epica', 'vostok', 'odp1012', 'odp1020']
labels = ['GRIP', 'NGRIP', 'EPICA', 'Vostok', 'ODP 1012', 'ODP 1020']
colors = ['#1F78B4', '#A6CEE3', '#E31A1C', '#FB9A99', '#33A02C', '#B2DF8A']
markers = ['s', 'D', 'o', 'h', 'v', '^']
offsets = [6.1, 6.5, 5.9, 5.9, 6.1, 6.0]

# default thickness threshold
thkth = 1.0
