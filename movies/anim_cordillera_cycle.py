#!/usr/bin/env python
# Copyright (c) 2014-2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera glacial cycle animation."""

import os
import multiprocessing as mp
import matplotlib.colors as mcolors
import cartowik.decorations as cde
import pismx.open
import utils


def draw(t):
    """Plot complete figure for given time."""

    # initialize figure
    fig, grid, cax, tsax = utils.subplots()
    twax = tsax.twiny()

    # contour levels
    levels = range(0, 5000, 200)
    majors = [lev for lev in levels if lev % 1000 == 0]
    minors = [lev for lev in levels if lev % 1000 != 0]

    # for each record
    for i, rec in enumerate(['GRIP', 'EPICA']):
        ax = grid[i]
        color = ['C1', 'C5'][i]
        offset = [6.2, 5.9][i]
        dtfile = '{:s}.3222.{:04d}'.format(rec.lower(), round(offset*100))
        rundir = '~/pism/output/0.7.2-craypetsc/ciscyc4.5km.{:s}.{:04d}/'
        rundir = rundir.format(rec.lower(), round(offset*100))

        # plot extra data
        # FIXME port alps util open_subdataset
        # FIXME port alps util shaded_relief
        with pismx.open.mfdataset(rundir+'ex.???????.nc') as ds:
            ds = ds.sel(age=-t/1e3)
            ds = ds.transpose(..., 'x')  # FIXME in pismx?
            ds.topg.plot.imshow(
                ax=ax, cmap='Greys', vmin=0e3, vmax=3e3, add_colorbar=False,
                zorder=-1)
            ds.usurf.where(ds.thk >= 1.0).plot.contour(
                ax=ax, colors=['0.25'], levels=majors, linewidths=0.25)
            ds.usurf.where(ds.thk >= 1.0).plot.contour(
                ax=ax, colors=['0.25'], levels=minors, linewidths=0.1)
            ds.thk.plot.contour(
                ax=ax, colors=['0.25'], levels=[1.0], linewidths=0.25)
            ds.velsurf_mag.where(ds.thk >= 1.0).plot.imshow(
                ax=ax, cmap='Blues', norm=mcolors.LogNorm(1e1, 1e3),
                alpha=0.75, cbar_ax=cax, cbar_kwargs=dict(
                    orientation='horizontal',
                    label=r'surface velocity ($m\,a^{-1}$)'))

        # add map elements
        utils.draw_natural_earth(ax, scale='50m')
        cde.add_subfig_label(rec, ax=ax, loc='nw')
        cde.add_subfig_label('{:.1f} ka'.format(-t/1e3), ax=ax, loc='ne')

        # plot temperature forcing
        with pismx.open.dataset('~/pism/input/dt/'+dtfile+'.nc') as ds:
            data = ds.delta_T[ds.time <= t]
            tsax.plot(data, data.age, color=color, alpha=0.25)
            tsax.text(data[-1], -t/1e3, '  {:.1f}°C'.format(float(data[-1])),
                      ha='left', va='center', clip_on=True, color=color)

        # plot ice volume time series
        with pismx.open.mfdataset(rundir+'/ts.???????.nc') as ds:
            data = ds.slvol[ds.age >= -t/1e3]
            twax.plot(data, data.age, color=color)
            twax.text(data[-1], -t/1e3, '  {:.1f} m'.format(float(data[-1])),
                      ha='left', va='center', clip_on=True, color=color)

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
