#!/usr/bin/env python
# Copyright (c) 2020-2024, Julien Seguinot (juseg.dev)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Prepare CISCYC continuous variables."""

import os
import sys
import datetime
import hyoga.open


def postprocess_extra(run):
    """Postprocess extra dataset for one run."""

    # variables to mask and not
    masked_vars = ['tempicethk_basal', 'temppabase', 'thk',
                   'uvelbase', 'uvelsurf', 'vvelbase', 'vvelsurf']
    nomask_vars = ['lon', 'lat', 'mapping', 'pism_config', 'topg']

    # global attributes
    _, res, rec, _ = os.path.basename(run).split('.')
    prefix = f'ciscyc.{res}.{rec}'
    cmd = ' '.join(sys.argv)
    time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    attributes = {
        'author':       'Julien Seguinot',
        'title':        'Cordilleran ice sheet glacial cycle simulations',
        'subtitle':     f'{res} {rec.upper()} simulation',
        'institution':  'Stockholm University, Sweden and '
                        'ETH Zürich, Switzerland',
        'command':      f'{os.getlogin()}@{os.uname()[1]} {time}: {cmd}\n'}

    # postprocess spatial diagnostics and time stamps
    print("postprocessing " + prefix + "...")
    with hyoga.open.mfdataset(run+'/ex.???????.nc') as ex:

        # select extra variables and ages
        ts = ex[['timestamp']]
        ex = ex[masked_vars+nomask_vars]
        ex = ex.transpose('age', 'y', 'x')

        # apply mask where needed
        for var in masked_vars:
            ex[var] = ex[var].where(ex.thk.fillna(0) >= 1)

        # assign attributes and export compressed file
        ex.attrs.update(history=attributes['command']+ex.history, **attributes)
        ex.attrs.update(title=ex.title + ' spatial diagnostics')
        ex.to_netcdf(prefix + '.ex.100a.nc', encoding={
            var: {'zlib': True} for var in ex.variables})

        # assign attributes and export compressed file
        ts.attrs.update(history=attributes['command']+ex.history, **attributes)
        ts.attrs.update(title=ex.title + ' time stamps')
        ts.to_netcdf(prefix + '.tms.nc', encoding={
            var: {'zlib': True} for var in ts.variables})

    # postprocess scalar time series
    with hyoga.open.mfdataset(run+'/ts.???????.nc') as ts:

        # assign attributes and export compressed file
        ts.attrs.update(history=attributes['command']+ts.history, **attributes)
        ts.attrs.update(title=ex.title + ' scalar time series')
        ts.to_netcdf(prefix + '.ts.10a.nc', encoding={
            var: {'zlib': True} for var in ts.variables})


def main():
    """Main program called during execution."""

    # create directory if missing
    os.makedirs('processed', exist_ok=True)
    os.chdir('processed')

    # postprocess selected runs
    for run in ['ciscyc4.10km.grip.0620', 'ciscyc4.10km.ngrip.0660',
                'ciscyc4.10km.epica.0590', 'ciscyc4.10km.vostok.0595',
                'ciscyc4.10km.odp1012.0615', 'ciscyc4.10km.odp1020.0605',
                'ciscyc4.5km.epica.0590', 'ciscyc4.5km.grip.0620']:
        postprocess_extra('~/pism/output/0.7.2-craypetsc/' + run)


if __name__ == '__main__':
    main()
