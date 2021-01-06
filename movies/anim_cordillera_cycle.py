#!/usr/bin/env python
# Copyright (c) 2014-2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera glacial cycle animation."""

import os
import multiprocessing as mp
import matplotlib.pyplot as plt
import cartowik.decorations as cde
import utils

# uplift contour levels and colors
levs = [-600.0, -400.0, -200.0, 0.0, 10.0, 20.0, 30.0]
cmap = plt.get_cmap('RdBu_r', len(levs)+1)
cols = cmap(range(len(levs)+1))


def draw(t):
    """Plot complete figure for given time."""

    # initialize figure
    fig, grid, cax, tsax = utils.subplots()
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
    for i, rec in enumerate(['GRIP', 'EPICA']):
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
        utils.draw_natural_earth(ax, scale='50m')
        cde.add_subfig_label(rec, ax=ax, loc='nw')
        cde.add_subfig_label('{:.1f} ka'.format(-t/1e3), ax=ax, loc='ne')

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


def main():
    """Main program for command-line execution."""

    # set default font size for uplift tag and colorbars
    # plt.rc('font', size=12)  # from alps

    # start and end of animation
    t0, t1, dt = -120000, -0, 100

    # output frame directories
    outdir = os.path.join(os.environ['HOME'], 'anim', 'anim_cordillera_cycle')

    # iterable arguments to save animation frames
    iter_args = [(draw, outdir, t) for t in range(t0+dt, t1+1, dt)]

    # create frame directory if missing
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # plot all frames in parallel
    with mp.Pool(processes=4) as pool:
        pool.starmap(utils.save_animation_frame, iter_args)


if __name__ == '__main__':
    main()
