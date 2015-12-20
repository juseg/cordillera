#!/usr/bin/env python2
# coding: utf-8

"""Utils and parameters for this project."""


from matplotlib.colors import LogNorm, Normalize
import hr
import io
import lr
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

# default thickness threshold
thkth = 1.0

# sensitivity test parameters
sens_configs = ['ccyc4+till1545',
                'ccyc4+rheocp10+till1545',
                'ccyc4+rheocp10+esia5+till1545',
                'ccyc4+d050+wmax05m+till1545',
                'ccyc4+d010+wmax01m+till1545']
sens_labels = ['default', 'hard ice', 'soft ice', 'sticky bed', 'slippy bed']
sens_colors = ['k', '#ff7f00', '#fdbf6f', '#6a3d9a', '#cab2d6']
