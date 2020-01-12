#!/usr/bin/env python
# Copyright (c) 2020, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Prepare CISCYC continuous variables."""

import os
import sys
import datetime
import pismx.open


def postprocess_extra(run):
    """Postprocess extra dataset for one run."""

    # global attributes
    conf, res, rec, *other = os.path.basename(run).split('.')
    prefix = '{}.{}.{}'.format(conf[:6], res, rec)
    prefix += ('.num1e21' if 'num1e21' in other else '')
    attributes = {
        'author':       'Julien Seguinot',
        'title':        'Cordilleran ice sheet glacial cycle simulations',
        'subtitle':     '{} {} simulation'.format(res, rec.upper()),
        'institution':  'Stockholm University, Sweden and '
                        'ETH Zürich, Switzerland',
        'command':      '{user}@{host} {time}: {cmdl}\n'.format(
            user=os.getlogin(), host=os.uname()[1], cmdl=' '.join(sys.argv),
            time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'))}

    # postprocess spatial diagnostics and time stamps
    print("postprocessing " + prefix + "...")
    with pismx.open.mfdataset(run+'/ex.???????.nc') as ex:

        # select topographic variables
        ex = ex[['lat', 'lon', 'mapping', 'pism_config',
                 'thk', 'topg', 'usurf']]

        # select Hole U1420A, 59°41.3399′N, 143°12.0599′W
        # data[:, j, i] "is not supported because the ordering of
        # dimensions [...] can vary between different arrays"
        # so we use dist.dims (differs between PISM 0.7 and 1.0).
        lon, lat = -143.200998, 59.688998
        dist = (ex.lat-lat)**2 + (ex.lon-lon)**2
        i, j = divmod(int(dist.argmin()), dist.shape[-1])
        ex = ex.isel({dist.dims[-2]: i, dist.dims[-1]: j})

        # assign attributes and export compressed file
        ex.attrs.update(history=attributes['command']+ex.history, **attributes)
        ex.attrs.update(title=ex.title + ' at IODP U1420A')
        ex.to_netcdf(prefix + '.iodp341.nc', encoding={var: dict(
            zlib=True, shuffle=True, complevel=1) for var in ex.variables})


def main():
    """Main program called during execution."""

    # create directory if missing
    os.makedirs('processed', exist_ok=True)
    os.chdir('processed')

    # postprocess selected runs
    # run 1.1.3/cisbed4.5km.epica.590.gou11simi.num1e21 has issues
    for run in ['0.7.2-craypetsc/ciscyc4.10km.{}',
                '1.1.3/cisbed4.10km.{}.gou11simi',
                '1.1.3/cisbed4.10km.{}.gou11simi.num1e21']:
        for forcing in ['epica.0590', 'grip.0620']:
            postprocess_extra('~/pism/output/'+run.format(forcing))


if __name__ == '__main__':
    main()
