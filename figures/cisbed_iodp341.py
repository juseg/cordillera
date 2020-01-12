#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Plot Cordillera bedrock IODP 341 time series."""

import os
import absplots as apl
import pismx.open
import util


def main():
    """Main program called during execution."""

    # initialize figure
    fig, tsax = apl.subplots_mm(figsize=(170, 60), gridspec_kw=dict(
        left=12.5, right=2.5, bottom=7.5, top=5, hspace=2.5, wspace=2.5))

    # for each record
    for i, rec in enumerate(util.cisbed_records):
        color = util.cisbed_colours[i]
        offset = util.cisbed_offsets[i]

        # for each configuration
        rundirs = ['0.7.2-craypetsc/ciscyc4.10km.{}.{:04.0f}',
                   '1.1.3/cisbed4.10km.{}.{:04.0f}.gou11simi',
                   '1.1.3/cisbed4.10km.{}.{:04.0f}.gou11simi.num1e21']
        for rundir in rundirs:
            color = 'C{:d}'.format(4*(rec == 'EPICA') + 1*('cisbed' in rundir))
            label = r'{}, {}, $\nu_m = 10^{{{}}}\,Pa\,s$'.format(
                rec, 'new' if 'cisbed' in rundir else 'old',
                '21' if 'num1e21' in rundir else '19')
            style = ':' if 'num1e21' in rundir else '-'

            # load ice volume time series
            # run 1.1.3/cisbed4.5km.epica.590.gou11simi.num1e21 has issues
            with pismx.open.mfdataset(
                    os.path.expanduser('~/pism/output/{}/ex.???????.nc'.format(
                        rundir.format(rec.lower(), 100*offset)))) as data:

                # select Hole U1420A, 59°41.3399′N, 143°12.0599′W
                # data[:, j, i] "is not supported because the ordering of
                # dimensions [...] can vary between different arrays"
                # so we use dist.dims (differs between PISM 0.7 and 1.0).
                lon, lat = -143.200998, 59.688998
                dist = (data.lat-lat)**2 + (data.lon-lon)**2
                i, j = divmod(int(dist.argmin()), dist.shape[-1])
                data = data.isel({dist.dims[-2]: i, dist.dims[-1]: j})

                # plot ice volume time series
                data.topg.plot(ax=tsax, color=color, label=label, ls=style)

    # set time series axes properties
    tsax.set_title('Model output at IODP U1420A, 59°41′N, 143°12′W')
    tsax.set_xlim(40.0, 0.0)
    tsax.legend()

    # save figure
    util.pl.savefig(fig)


if __name__ == '__main__':
    main()
