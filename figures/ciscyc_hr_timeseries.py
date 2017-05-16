#!/usr/bin/env python2
# coding: utf-8

import util as ut
import iceplotlib.plot as iplt

# initialize time-series figure
figw, figh = 85.0, 80.0
fig, (ax1, ax2) = iplt.subplots_mm(nrows=2, ncols=1, sharex=True,
                                   figsize=(figw, figh),
                                   left=10.0, right=2.5, bottom=10.0, top=2.5,
                                   wspace=2.5, hspace=2.5)

# loop on records
for i, rec in enumerate(ut.ciscyc_hr_records):
    dt = ut.ciscyc_hr_offsets[i]
    c = ut.ciscyc_hr_colours[i]

    # plot forcing time series
    nc = ut.io.load('input/dt/%s3222cool%04d.nc'
                    % (rec.replace(' ', '').lower(), round(100*dt)))
    dt_time = nc.variables['time'][:]*1e-3
    dt_temp = nc.variables['delta_T'][:]
    nc.close()
    ax1.plot(-dt_time, dt_temp, color=c, label=rec)

    # plot output time series
    for res in ('10km', '5km'):
        nc = ut.io.load('output/0.7.2-craypetsc/cordillera-narr-5km/'
                        '%s3222cool%03d+ccyc4+till1545/y???????-ts.nc'
                         % (rec.replace(' ', '').lower(), round(100*dt)))
        ts_time = nc.variables['time'][:]*ut.s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        ax2.plot(-ts_time, ts_ivol, color=c,
                 dashes=((None, None) if res == '10km' else (1, 1)),
                 label='%s %s' % (rec, res))

# set axes properties and save time series
ax2.invert_xaxis()
ax1.set_xlim(25.0, 5.0)
ax2.set_xlim(25.0, 5.0)
ax1.set_ylim(-10.0, 2.0)
ax2.set_ylim(0.0, 9.5)
ax1.set_ylabel('temperature offset (K)')
ax2.set_ylabel('ice volume (m s.-l. eq.)')
ax1.yaxis.set_label_coords(-0.075, 0.5)
ax2.yaxis.set_label_coords(-0.075, 0.5)
ax2.set_xlabel('model age (ka)')
ax2.legend(loc='upper right', bbox_to_anchor=(1, 1+2.5/32.5))
ax1.grid(axis='y')
ax2.grid(axis='y')
ut.pl.savefig(fig)
