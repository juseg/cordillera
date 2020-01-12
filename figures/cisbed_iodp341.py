#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Plot Cordillera bedrock IODP 341 time series."""

import glob
import xarray as xr
import absplots as apl
import util


def main():
    """Main program called during execution."""

    # initialize figure
    fig, tsax = apl.subplots_mm(figsize=(170, 60), gridspec_kw=dict(
        left=12.5, right=2.5, bottom=7.5, top=5, hspace=2.5, wspace=2.5))

    # for each run
    for run in sorted(glob.glob('../data/processed/*.iodp341.nc')):
        color = 'C{:d}'.format(4*('epica' in run) + 1*('cisbed' in run))
        label = r'{}, {}, $\nu_m = 10^{{{}}}\,Pa\,s$'.format(
            'EPICA' if 'epica' in run else 'GRIP',
            'new' if 'cisbed' in run else 'old',
            '21' if 'num1e21' in run else '19')
        style = ':' if 'num1e21' in run else '-'

        # plot ice volume time series
        with xr.open_dataset(run) as data:
            data.topg.plot(ax=tsax, color=color, label=label, ls=style)

    # set time series axes properties
    tsax.set_title('Model output at IODP 341, hole U1420A, 59°41′N, 143°12′W')
    tsax.set_xlim(40.0, 0.0)
    tsax.legend()

    # save figure
    util.pl.savefig(fig)


if __name__ == '__main__':
    main()
