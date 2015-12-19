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
offsets = [6.2, 6.6, 5.9, 6.0, 6.1, 6.0]

# high-resolution run selector
hrs = slice(0, 3, 2)

# default thickness threshold
thkth = 1.0

# sensitivity test parameters
sens_configs = ['ccyc4+till1545',
                'ccyc4+rheocp10+esia2+till1545',
                'ccyc4+rheocp10+esia5+till1545',
                'ccyc4+rheocp10+till1545',
                'ccyc4+till3030',
                'ccyc4+d010+till1545',
                'ccyc4+d050+till1545',
                'ccyc4+wmax01m+till1545',
                'ccyc4+wmax05m+till1545']
sens_labels = ['dflt', 'CP10', '2CP10', '5CP10',
               'phi30', 'd01', 'd05', 'wmax1', 'wmax5']
sens_colors = ['k'] + ['#6a3d9a']*3 + ['#ff7f00']*3 + ['#b15928']*2
