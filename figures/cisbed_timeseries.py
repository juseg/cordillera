#!/usr/bin/python
# Copyright (c) 2019-2023, Julien Seguinot (juseg.dev)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera bedrock ice volume time series."""

import absplots as apl
import hyoga.open


def main():
    """Main program called during execution."""

    # initialize figure
    fig, ax = apl.subplots_mm(figsize=(170, 60), gridspec_kw=dict(
        left=10, right=10, bottom=7.5, top=2.5, hspace=2.5, wspace=2.5))

    # select runs that are not broken
    # FIXME cisbed4.5km.epica.590.gou11simi.num1e21 has non-increasing times
    # FIXME cisbed4.3km.grip.0620.gou11simi.num1e21 has different pism_config?!
    # FIXME cisbed4.3km.epica.0620.gou11simi.num1e21 has different mappings?!
    for run in [
        '0.7.2-craypetsc/ciscyc4.10km.grip.0620',
        '1.1.3/cisbed4.10km.grip.0620.ghf70',
        '1.1.3/cisbed4.3km.grip.0620.gou11simi.num1e21',
        '0.7.2-craypetsc/ciscyc4.10km.epica.0590',
        '1.1.3/cisbed4.10km.epica.0590.ghf70',
        '1.1.3/cisbed4.3km.epica.0590.gou11simi.num1e21']:

        # open ts output
        with hyoga.open.mfdataset('~/pism/output/'+run+'/ts.*.nc') as ds:

            # plot ice volume time series
            ds.get('sea_level_rise_potential', ds.get('slvol')).plot(
                ax=ax, alpha=1 if 'cisbed' in run else 0.5,
                color='tab:blue' if 'grip' in run else 'tab:red',
                ls=':' if '3km' in run else '-',
                label=', '.join([
                    'EPICA' if 'epica' in run else 'GRIP',
                    'old' if 'ciscyc' in run else
                    'fixed' if 'ghf70' in run else 'improved']))

    # set axes properies
    ax.grid(axis='y')
    ax.legend(loc='best')
    ax.set_xlabel('model age (ka)', labelpad=2)
    ax.set_xlim(30, 0)
    ax.set_ylabel('ice volume (m s.l.e.)')

    # save
    fig.savefig(__file__[:-3])


if __name__ == '__main__':
    main()
