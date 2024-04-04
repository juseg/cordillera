#!/usr/bin/python
# Copyright (c) 2023, Julien Seguinot (juseg.dev)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera bedrock surface mass balance."""

import absplots as apl
import hyoga.open
import util


def main():
    """Main program called during execution."""

    # initialize figure
    fig, axes = apl.subplots_mm(
        figsize=(177, 80), nrows=2, ncols=3, sharex=True, sharey=True,
        gridspec_kw={
            'left': 1.5, 'right': 1.5, 'bottom': 1, 'top': 1.5,
            'hspace': 1.5, 'wspace': 1.5})
    cax = fig.add_axes_mm([57*2+19+1.5*4, 38/3-3, 57*2/3-1.5, 3])

    # for each selected age
    for ax, age in zip(axes.flat, range(16, 10, -1)):

        # open extra output
        with hyoga.open.subdataset(
                '~/pism/output/1.1.3/cisbed4.5km.grip.0620.ghf70/'
                'ex.{:07.0f}.nc', time=-age*1e3, shift=120000) as ds:

            # plot ice geometry
            ds.hyoga.plot.bedrock_altitude(ax=ax, vmin=0, vmax=4500)
            ds.hyoga.plot.ice_margin(ax=ax)
            ds.hyoga.plot.surface_altitude_contours(ax=ax)

            # plot surface runoff
            ds.surface_runoff_flux.where(ds.thk > 1).plot.imshow(
                ax=ax, cmap='Reds', vmin=0, vmax=6e3,
                cbar_ax=cax, cbar_kwargs={
                    'label': r'surface runoff ($kg\,m^{-2}\,a{-1}$)',
                    'orientation': 'horizontal'})

            # plot equilibrium line
            (ds.surface_accumulation_flux - ds.surface_melt_flux).where(
                ds.thk > 1).plot.contour(
                    ax=ax, colors='0.25', levels=[0], linestyles='--')

            # add coastline and rivers
            ax = ds.hyoga.plot.natural_earth(ax=ax)

        # set axes properties
        util.pl.add_subfig_label(f'{age:.1f} ka', ax=ax)
        ax.set_title('')
        ax.set_xlim(-2200e3, -1300e3)
        ax.set_ylim(300e3, 900e3)

    # save
    fig.savefig(__file__[:-3])


if __name__ == '__main__':
    main()
