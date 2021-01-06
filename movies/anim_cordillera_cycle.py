#!/usr/bin/env python2
# coding: utf-8

import os
import utils as ut
import multiprocessing as mp
import matplotlib.pyplot as plt

# uplift contour levels and colors
levs = [-600.0, -400.0, -200.0, 0.0, 10.0, 20.0, 30.0]
cmap = ut.pl.get_cmap('RdBu_r', len(levs)+1)
cols = cmap(range(len(levs)+1))


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

        # plot
        im = nc.imshow('topg', ax, t, vmin=0.0, vmax=3e3, cmap='Greys', zorder=-1)
        cs = nc.contour('topg', ax, t, levels=[0.0], colors='0.25',
                        linewidths=0.25, zorder=0)
        im = nc.imshow('velsurf_mag', ax, t, norm=ut.pl.velnorm, cmap='Blues',
                       alpha=0.75)
        cs = nc.contour('usurf', ax, t, levels=ut.pl.inlevs,
                        colors='0.25', linewidths=0.1)
        cs = nc.contour('usurf', ax, t, levels=ut.pl.utlevs,
                        colors='0.25', linewidths=0.25)
        cs = nc.icemargin(ax, t, colors='k', linewidths=0.25)

        # close extra data
        nc.close()

        # add map elements
        ut.pl.draw_natural_earth(ax)
        ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (rec, 0.0-t/1e3))

        # load temperature forcing
        nc = ut.io.load('input/dt/%s.nc' % dt_file)
        age = -nc.variables['time'][:]/1e3
        dt = nc.variables['delta_T'][:]
        nc.close()

        # plot temperature forcing
        mask = age>=-t/1e3
        tsax.plot(dt[mask], age[mask], color=c, alpha=0.25)

        # load time series data
        nc = ut.io.load(run_dir + '/y???????-ts.nc')
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)
        vol = nc.variables['slvol'][:]
        nc.close()

        # plot ice volume time series
        mask = age>=-t/1e3
        twax.plot(vol[mask], age[mask], color=c)

    # add colorbar
    cb = fig.colorbar(im, cax, extend='both', orientation='horizontal')
    cb.set_label(r'surface velocity ($m\,a^{-1}$)')

    # set time series axes properties
    tsax.set_ylim(120.0, 0.0)
    tsax.set_xlim(-9.5, 0.5)
    tsax.set_ylabel('model age (ka)')
    tsax.set_xlabel('temperature offset (K)', color='0.75')
    tsax.yaxis.tick_right()
    tsax.yaxis.set_label_position('right')
    tsax.tick_params(axis='x', colors='0.75')
    tsax.grid(axis='x')

    # set twin axes properties
    twax.set_xlim(9.5, -0.5)
    twax.set_xlabel('ice volume (m s.l.e.)')

    # return figure
    return fig


def saveframe(years):
    """Independently plot one frame."""

    # check if file exists
    framename = '{:06d}.png'.format(years)
    framepath = '/scratch_net/iceberg/juliens/anim/anim_cordillera_cycle/' + framename
    if os.path.isfile(framepath):
        return

    # plot
    t = years - 120e3
    print 'plotting at %.1f ka...' % (0.0-t/1e3)
    fig = draw(t)

    # save
    fig.savefig(framepath)
    plt.close(fig)


if __name__ == '__main__':
    """Plot individual frames in parallel."""

    # plot in parallel
    dt = 100
    pool = mp.Pool(processes=12)
    pool.map(saveframe, xrange(dt, 120001, dt))
    pool.close()
    pool.join()
