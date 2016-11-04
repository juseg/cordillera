#!/usr/bin/env python2
# coding: utf-8

"""Utils and parameters for this project."""


from matplotlib.colors import LogNorm, Normalize
import hr
import io
import lr
import pl
import sens

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
