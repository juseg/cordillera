#!/usr/bin/env python
# Copyright (c) 2017-2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera glacial cycle animation."""

import os
import utils as ut
import multiprocessing as mp
import matplotlib.pyplot as plt

# uplift contour levels and colors
levs = [-600.0, -400.0, -200.0, 0.0, 10.0, 20.0, 30.0]
cmap = plt.get_cmap('RdBu_r', len(levs)+1)
cols = cmap(range(len(levs)+1))


def get_depression_ts():
    """Compute depression time-series. This need to be done once and for all
    in order to avoid a memory error."""

    # load boot topo
    filepath = 'input/boot/cordillera-etopo1bed+thk+gou11simi-5km.nc'
    nc = ut.io.load(filepath)
    zref = nc.variables['topg'][:].T
    nc.close()

    # for each record
    exage = []
    exdep = []
    for i, rec in enumerate(ut.cisbed_records):
        c = ut.cisbed_colours[i]
        dt = ut.cisbed_offsets[i]
        dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))
        run_dir = 'output/e9d2d1f/cordillera-narr-5km/%s+cisbed2+till1545' % dt_file

        # load bedrock topography
        nc = ut.io.load(run_dir + '/y???????-extra.nc')
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        z = nc.variables['topg'][:]
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)
        nc.close()

        # compute bedrock depression time series
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        dep = (zref-z).sum(axis=(1, 2))*dx*dy*1e-12

        # append to lists
        exage.append(age)
        exdep.append(dep)

    # return extra age and depression series
    return exage, exdep


def draw(t):
    """Plot complete figure for given time."""

    # initialize figure
    fig, grid, cax, tsax = ut.subplots_2_cax_ts_anim()
    twax = tsax.twiny()

    # add signature #FIXME move to util
    figw, figh = [dim*25.4 for dim in fig.get_size_inches()]
    fig.text(1-2.5/figw, 2.5/figh, 'J. Seguinot et al. (in prep.)',
             ha='right', va='bottom')

    # load boot topo
    filepath = 'input/boot/cordillera-etopo1bed+thk+gou11simi-5km.nc'
    nc = ut.io.load(filepath)
    zref = nc.variables['topg'][:].T
    nc.close()

    # for each record
    for i, rec in enumerate(ut.cisbed_records):
        ax = grid[i]
        c = ut.cisbed_colours[i]
        dt = ut.cisbed_offsets[i]
        dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))
        run_dir = 'output/e9d2d1f/cordillera-narr-5km/%s+cisbed2+till1545' % dt_file

        # load extra data
        nc = ut.io.load(run_dir + '/y???????-extra.nc')
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        z = nc.variables['topg'][:]
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)

        # plot uplift map
        x, y, z = nc._extract_xyz('topg', t)
        im = nc.imshow('topg', ax, t, vmin=0.0, vmax=3e3, cmap='Greys', zorder=-1)
        cs = nc.contour('topg', ax, t, levels=[0.0], colors='0.25',
                        linewidths=0.25, zorder=0)
        im = ax.contourf(x, y, z-zref, levels=levs, extend='both',
                         colors=cols, alpha=0.75)
        cs = nc.contour('usurf', ax, t, levels=ut.pl.inlevs,
                        colors='0.25', linewidths=0.1)
        cs = nc.contour('usurf', ax, t, levels=ut.pl.utlevs,
                        colors='0.25', linewidths=0.25)
        cs = nc.icemargin(ax, t, colors='k', linewidths=0.25)

        # locate maximum depression
        j = (z-zref).argmin() / z.shape[-1]
        k = (z-zref).argmin() % z.shape[-1]
        maxdep = (zref-z)[j, k]
        maxcol = 'w' if maxdep > -levs[1] else 'k'
        ax.plot(x[k], y[j], 'o', c=maxcol, alpha=0.75)
        ax.text(x[k]+5e3, y[j]+5e3, '{:.0f} m'.format(maxdep), color=maxcol)

        # close extra data
        nc.close()

        # add map elements
        ut.pl.draw_natural_earth(ax)
        ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (rec, 0.0-t/1e3))

        # load time series data
        nc = ut.io.load(run_dir + '/y???????-ts.nc')
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)
        vol = nc.variables['slvol'][:]
        nc.close()

        # plot ice volume time series
        mask = age>=-t/1e3
        tsax.plot(vol[mask], age[mask], color=c, alpha=0.25)

        # plot bedrock depression time series
        mask = exage[i]>=-t/1e3
        twax.plot(exdep[i][mask], exage[i][mask], c=c)

    # add colorbar
    cb = fig.colorbar(im, cax, orientation='horizontal')
    cb.set_label('bedrock uplift (m)')

    # set time series axes properties
    tsax.set_ylim(120.0, 0.0)
    tsax.set_xlim(9.5, -0.5)
    tsax.set_ylabel('model age (ka)')
    tsax.set_xlabel('ice volume (m s.l.e.)', color='0.75')
    tsax.yaxis.tick_right()
    tsax.yaxis.set_label_position('right')
    tsax.tick_params(axis='x', colors='0.75')
    tsax.grid(axis='x')

    # set twin axes properties
    twax.set_xlim(950.0, -50.0)
    twax.set_xlabel('volumic depression ($10^{3}\,km^{3}$)')

    # return figure
    return fig


def saveframe(years):
    """Independently plot one frame."""

    # check if file exists
    framename = '{:06d}.png'.format(years)
    framepath = '/scratch_net/iceberg/juliens/anim/anim_cordillera_uplift/' + framename
    if os.path.isfile(framepath):
        return

    # plot
    t = years - 120e3
    print('plotting at %.1f ka...' % (0.0-t/1e3))
    fig = draw(t)

    # save
    fig.savefig(framepath)
    plt.close(fig)


if __name__ == '__main__':
    """Plot individual frames in parallel."""

    # compute depression time-series
    print('computing depression time-series...')
    exage, exdep = get_depression_ts()

    # plot in parallel
    dt = 100
    pool = mp.Pool(processes=12)
    pool.map(saveframe, range(dt, 120001, dt))
    pool.close()
    pool.join()
