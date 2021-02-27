#!/usr/bin/env python
# Copyright (c) 2014-2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera cycle zoom on Puget Lowland."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartowik.decorations as cde
import cartowik.naturalearth as cne
import cartowik.shadedrelief as csr
import absplots as apl
import hyoga.open


def main():
    """Main program called during execution."""

    # initialize figure
    fig, grid = apl.subplots_mm(
        nrows=2, ncols=5, sharex=True, sharey=True, figsize=(177, 71),
        gridspec_kw=dict(
            left=1, right=1, bottom=1, top=1, wspace=1, hspace=1),
        subplot_kw=dict(projection=ccrs.LambertConformal(
            central_longitude=-95, central_latitude=49,
            standard_parallels=(49, 77))))

    # for each selected age
    for i, ax in enumerate(grid.flat):
        age = 20 - i/2

        # set extent and add labels
        ax.set_extent([-2175e3, -1875e3, 225e3, 525e3], crs=ax.projection)

        # get interpolated sea level
        with hyoga.open.dataset('~/pism/input/dsl/specmap.nc') as ds:
            dsl = ds.delta_SL.interp(age=age, method='linear')

        # plot interpolated model output
        with hyoga.open.subdataset(
                ('~/pism/output/0.7.2-craypetsc/'
                 'ciscyc4.5km.epica.0590/ex.{:07.0f}.nc'),
                time=-age*1e3, shift=120000) as ds:

            # get isostasy, mask and interpolate
            ds = ds.hyoga.assign_isostasy(
                '~/pism/input/boot/cordillera.etopo1bed.hus12.5km.nc')
            ds = ds.hyoga.interp(
                '~/pism/input/boot/cordillera.etopo1bed.hus12.1km.nc', ax=ax)

            # shaded relief and coastline
            (ds.topg-dsl).plot.imshow(
                ax=ax, add_colorbar=False, zorder=-1,
                cmap=mcolors.LinearSegmentedColormap.from_list('Elevational', [
                    *plt.get_cmap('Blues_r')(np.linspace(0, 1, 2048)),
                    *plt.get_cmap('Greys')(np.linspace(0, 1, 2048))], N=4096),
                norm=mcolors.TwoSlopeNorm(vmin=-600., vcenter=0, vmax=3000))
            csr.add_multishade(
                ds.topg, ax=ax, add_colorbar=False, zorder=-1)
            ds.topg.plot.contour(
                ax=ax, colors='0.25',
                levels=[dsl], linestyles='solid', linewidths=0.25, zorder=0)

            # ice margin and contour levels
            ds.thk.notnull().plot.contour(
                ax=ax, colors=['0.25'], levels=[0.5], linewidths=0.25)
            ds.thk.notnull().plot.contourf(
                ax=ax, add_colorbar=False, alpha=0.75, colors='w',
                extend='neither', levels=[0.5, 1.5])
            ds.usurf.plot.contour(
                levels=[lev for lev in range(0, 5000, 200) if lev % 1000 == 0],
                ax=ax, colors=['0.25'], linewidths=0.25)
            ds.usurf.plot.contour(
                levels=[lev for lev in range(0, 5000, 200) if lev % 1000 != 0],
                ax=ax, colors=['0.25'], linewidths=0.1)

            # velocity stream plot
            ax.streamplot(
                ds.x, ds.y,
                ds.uvelsurf.to_masked_array(), ds.vvelsurf.to_masked_array(),
                color=((ds.uvelsurf**2+ds.vvelsurf**2)**0.5).to_masked_array(),
                cmap='Reds', norm=mcolors.LogNorm(1e2, 1e4),
                arrowsize=0.25, linewidth=0.5, density=(3, 3))

        # add map element
        kwargs = dict(ax=ax, scale='10m', zorder=0)
        cne.add_coastline(edgecolor='0.25', linestyle='dashed', **kwargs)
        cde.add_subfig_label('{:.1f} ka'.format(age), ax=ax, loc='sw')
        ax.set_title('')

    # save
    fig.savefig(__file__[:-3])


if __name__ == '__main__':
    main()
