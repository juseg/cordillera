#!/usr/bin/python
# Copyright (c) 2015-2023, Julien Seguinot (juseg.dev)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera bedrock computing time stamps."""

import absplots as apl
import hyoga.open


def main():
    """Main program called during execution."""

    # initialize figure
    fig, ax = apl.subplots_mm(figsize=(85, 80), gridspec_kw=dict(
            left=12, right=1.5, bottom=12, top=1.5))

    # select runs that are not broken
    # FIXME cisbed4.5km.epica.590.gou11simi.num1e21 has non-increasing times
    # FIXME cisbed4.3km.grip.0620.gou11simi.num1e21 has different pism_config?!
    # FIXME cisbed4.3km.epica.0620.gou11simi.num1e21 has different mappings?!
    for run in ['cisbed4.10km.grip.0620.gou11simi',
                'cisbed4.10km.epica.0590.gou11simi',
                'cisbed4.5km.grip.0620.gou11simi',
                'cisbed4.5km.epica.0590.gou11simi',
                'cisbed4.3km.grip.0620.gou11simi.num1e21',
                'cisbed4.3km.epica.0590.gou11simi.num1e21']:

        # open extra output
        with hyoga.open.mfdataset(
                '~/pism/output/1.1.3/{}/ex.*.nc'.format(run),
                coords='minimal', compat='override') as ds:
            diff = ds.timestamp.diff('age')
            procs = ds['rank'].max() + 1
            stamp = diff.where(diff > 0, ds.timestamp[1:]).cumsum()
            stamp.plot(
                ax=ax, color='C0' if 'grip' in run else 'C2',
                label=r'{}, {}, {:d} cores, {:.0f} kch'.format(
                    run.split('.')[1], run.split('.')[2].upper(), int(procs),
                    float(procs*stamp[-1]/1e3)))

    # set axes properies
    ax.invert_xaxis()
    ax.set_xlabel('model age (ka)')
    ax.set_ylabel('computing time (hours)')
    ax.legend(loc='best')

    # save
    fig.savefig(__file__[:-3])


if __name__ == '__main__':
    main()
