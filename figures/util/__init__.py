# Copyright (c) 2014--2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Utils and parameters for the Cordillera project."""


from matplotlib.colors import LogNorm, Normalize
import util.io  # input and output
import util.pl  # plotting tools

# unit conversion
# FIXME: use iplt.subplots_mm instead
in2mm = 1/25.4
pt2mm = 72*in2mm
a2s = 365.0 * 24 * 60 * 60
s2a = 1/a2s
s2ka = s2a/1e3

# colors
# FIXME: move to ut.pl
topo_cmap = 'Greys'
topo_norm = Normalize(-3000, 6000)
vel_cmap = 'RdBu_r'
vel_norm = LogNorm(1e1, 1e3)

# default thickness threshold
# FIXME: this should not be needed with newer iceplotlib
thkth = 1.0


# Cordillera bedrock parameters
# -----------------------------

# low (10km) resolution runs
cisbed_records = ['GRIP', 'EPICA']
cisbed_offsets = [6.2, 5.9]
cisbed_markers = ['s', 'o']
cisbed_colours = ['C1', 'C5']  # darkblue, darkred


# Cordillera cycle parameters
# ---------------------------

# low (10km) resolution runs
ciscyc_lr_records = ['GRIP', 'NGRIP', 'EPICA', 'Vostok',
                     'ODP 1012', 'ODP 1020']
ciscyc_lr_offsets = [6.2, 6.6, 5.9, 5.95, 6.15, 6.05]
ciscyc_lr_markers = ['s', 'D', 'o', 'h', 'v', '^']
ciscyc_lr_colours = ['C1', 'C0', 'C5', 'C4', 'C3', 'C2']  # db lb dr lr dg lg

# high (5km) resolution runs
ciscyc_hr_records = ciscyc_lr_records[0:3:2]
ciscyc_hr_offsets = ciscyc_lr_offsets[0:3:2]
ciscyc_hr_markers = ciscyc_lr_markers[0:3:2]
ciscyc_hr_colours = ciscyc_lr_colours[0:3:2]

# sensitivity study runs
ciscyc_sens_configs = ['ccyc4%s+till1545' % c
                       for c in ['', '+rheocp10+esia5', '+rheocp10',
                                 '+d010+wmax01m', '+d050+wmax05m']]
ciscyc_sens_offsets = [6.2, 6.65, 5.95, 6.55, 5.85]
ciscyc_sens_clabels = ['Default', 'Soft ice', 'Hard ice',
                       'Soft bed', 'Hard bed']
ciscyc_sens_colours = ['0.25', '#cab2d6', '#6a3d9a', '#fdbf6f', '#ff7f00']
