#!/usr/bin/env python
# Copyright (c) 2014-2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

"""Cordillera two-panel animation framework."""

import os
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartowik.decorations as cde
import cartowik.naturalearth as cne
import absplots as apl
import pismx.open


# Color palette
# -------------

# set color cycle to colorbrewer Paired palette
plt.rc('axes', prop_cycle=plt.cycler(color=plt.get_cmap('Paired').colors))


# Figure saving
# -------------

def save_animation_frame(func, outdir, t, *args, **kwargs):
    """Save figure produced by func as animation frame if missing."""

    # check if file exists
    fname = os.path.join(outdir, '{:06d}.png').format(t+120000)
    if not os.path.isfile(fname):

        # assemble figure and save
        print('plotting {:s} ...'.format(fname))
        fig = func(t, *args, **kwargs)
        fig.savefig(fname)
        plt.close(fig)


# Main visual
# -----------

def draw(t):
    """Plot complete figure for given time."""

    # initialize figure (108*1500/2700=60)
    fig, grid = apl.subplots_mm(
        ncols=2, nrows=1, sharex=True, sharey=True, figsize=(192, 108),
        gridspec_kw=dict(left=0, right=192-120, bottom=0, top=0, wspace=0),
        subplot_kw=dict(projection=ccrs.LambertConformal(
            central_longitude=-95, central_latitude=49,
            standard_parallels=(49, 77))))
    tsax = fig.add_axes_mm([120+10, 30, 192-120-20, 108-40])
    cax = fig.add_axes_mm([120+10, 15, 192-120-20, 5])

    # prepare map axes
    for i, ax in enumerate(grid):
        ax.set_extent([-2500e3, -1000e3, 150e3, 2850e3], crs=ax.projection)
        ax.spines['geo'].set_ec('none')

    # add delimitors on last axes
    for i in range(2):
        ax.plot([i, i], [0, 1], color='k', clip_on=False,
                transform=ax.transAxes, zorder=3)
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
        cne.add_rivers(ax=ax, edgecolor='0.25', zorder=0, scale='50m')
        cne.add_lakes(ax=ax, edgecolor='0.25', facecolor='0.95', zorder=0,
                      scale='50m')
        cne.add_coastline(ax=ax, edgecolor='0.25', zorder=0, scale='50m')
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

    # start and end of animation
    t0, t1, dt = -120000, -0, 10000

    # output frame directories
    outdir = os.path.join(os.environ['HOME'], 'anim', 'anim_cordillera_dual')

    # iterable arguments to save animation frames
    iter_args = [(draw, outdir, t) for t in range(t0+dt, t1+1, dt)]

    # create frame directory if missing
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # plot all frames in parallel
    with mp.Pool(processes=4) as pool:
        pool.starmap(save_animation_frame, iter_args)


if __name__ == '__main__':
    main()
