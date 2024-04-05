#!/usr/bin/env python
# Copyright (c) 2020-2024, Julien Seguinot (juseg.dev)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Prepare CISCYC continuous variables."""

import os
import sys
import datetime
import hyoga.open


def postprocess(run):
    """Postprocess spatial diagnostics and timeseries for one run."""

    # variables to mask and not
    masked_vars = ['bmelt', 'surface_accumulation_flux', 'surface_runoff_flux',
                   'tempicethk_basal', 'temppabase', 'thk', 'tillwat',
                   'uvelbase', 'uvelsurf', 'vvelbase', 'vvelsurf']
    nomask_vars = ['lon', 'lat', 'mapping', 'pism_config', 'topg']

    # global attributes
    _, res, rec, _, *config = os.path.basename(run).split('.')
    prefix = f'cisbed.{res}.{rec}.' + '.'.join(config)
    cmd = ' '.join(sys.argv)
    time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    attributes = {
        'author':       'Julien Seguinot',
        'title':        'Cordilleran ice sheet improved bedrock simulations',
        'subtitle':     f'{res} {rec.upper()} simulation',  # FIXME details
        'institution':
            'Laboratory of Hydraulics, Hydrology and Glaciology (VAW), ETH '
            'Zürich, Zurich, Switzerland and Department of Water and Climate, '
            'Vrije Universiteit Brussel, Brussels, Belgium',
        'command':      f'{os.getlogin()}@{os.uname()[1]} {time}: {cmd}\n'}

    # postprocess spatial diagnostics and time stamps
    print("postprocessing " + prefix + "...")
    with hyoga.open.mfdataset(run+'/ex.???????.nc') as ex:

        # select extra variables and ages
        ts = ex[['timestamp']]
        ex = ex[masked_vars+nomask_vars]

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
    for run in [
            'cisbed4.10km.epica.0590.ghf70', 'cisbed4.10km.grip.0620.ghf70',
            'cisbed4.5km.epica.0590.ghf70', 'cisbed4.5km.grip.0620.ghf70']:
        postprocess('~/pism/output/1.1.3/' + run)


if __name__ == '__main__':
    main()
