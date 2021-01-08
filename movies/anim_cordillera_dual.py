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

def save_animation_frame(func, outdir, time, *args, **kwargs):
    """Save figure produced by func as animation frame if missing."""

    # check if file exists
    fname = os.path.join(outdir, '{:06d}.png').format(time+120000)
    if not os.path.isfile(fname):

        # assemble figure and save
        print('plotting {:s} ...'.format(fname))
        fig = func(time, *args, **kwargs)
        fig.savefig(fname)
        plt.close(fig)


# Main visual
# -----------

def draw(time):
    """Plot complete figure for given time."""

    # initialize figure (108*1500/2700=60)
    fig, grid = apl.subplots_mm(
        ncols=2, nrows=1, sharex=True, sharey=True, figsize=(192, 108),
        gridspec_kw=dict(left=0, right=192-120, bottom=0, top=0, wspace=0),
        subplot_kw=dict(projection=ccrs.LambertConformal(
            central_longitude=-95, central_latitude=49,
            standard_parallels=(49, 77))))
    cax = fig.add_axes_mm([120+5, 15, 192-120-20, 5])
    tsax = fig.add_axes_mm([120+5, 30, 192-120-20, 108-40])
    twax = tsax.twiny()

    # prepare map axes
    for i, ax in enumerate(grid):
        ax.set_extent([-2500e3, -1000e3, 150e3, 2850e3], crs=ax.projection)
        ax.spines['geo'].set_ec('none')
        fig.lines.append(plt.Line2D([1, 1], [0, 1], transform=ax.transAxes))

    # for each record
    for i, rec in enumerate(['GRIP', 'EPICA']):
        ax = grid[i]
        color = ['C1', 'C5'][i]
        offset = [6.2, 5.9][i]
        dtfile = '{:s}.3222.{:04d}'.format(rec.lower(), round(offset*100))
        rundir = '~/pism/output/0.7.2-craypetsc/ciscyc4.5km.{:s}.{:04d}/'
        rundir = rundir.format(rec.lower(), round(offset*100))

        # plot extra data
        # FIXME port alps util open_visual
        # FIXME port alps util shaded_relief
        with pismx.open.subdataset(
                rundir+'ex.{:07.0f}.nc', time, shift=120000) as ds:
            ds = ds.transpose(..., 'x')  # FIXME in pismx?
            ds.topg.plot.imshow(
                ax=ax, cmap='Greys', vmin=0e3, vmax=3e3, add_colorbar=False,
                zorder=-1)
            ds.usurf.where(ds.thk >= 1.0).plot.contour(
                levels=[lev for lev in range(0, 5000, 200) if lev % 1000 == 0],
                ax=ax, colors=['0.25'], linewidths=0.25)
            ds.usurf.where(ds.thk >= 1.0).plot.contour(
                levels=[lev for lev in range(0, 5000, 200) if lev % 1000 != 0],
                ax=ax, colors=['0.25'], linewidths=0.1)
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

        # plot temperature forcing
        with pismx.open.dataset('~/pism/input/dt/'+dtfile+'.nc') as ds:
            data = ds.delta_T[ds.time <= time]
            tsax.plot(data, data.age, color=color, alpha=0.25)
            tsax.text(data[-1], -time/1e3, '{:.1f}°C'.format(float(data[-1])),
                      ha='center', va='bottom', clip_on=True, color=color,
                      alpha=0.25)

        # plot ice volume time series
        with pismx.open.mfdataset(rundir+'/ts.???????.nc') as ds:
            data = ds.slvol[ds.age >= -time/1e3]
            twax.plot(data, data.age, color=color)
            twax.text(data[-1], -time/1e3, '{:.1f} m'.format(float(data[-1])),
                      ha='center', va='bottom', clip_on=True, color=color)

    # set time series axes properties
    tsax.set_ylim(120.0, 0.0)
    tsax.set_xlim(-9.5, 1.5)
    tsax.set_xlabel('temperature change (°C)', color='0.75')
    tsax.yaxis.tick_right()
    tsax.yaxis.set_label_position('right')
    tsax.tick_params(axis='x', colors='0.75')
    tsax.grid(axis='x')

    # set twin axes properties
    twax.set_xlim(-1.5, 9.5)
    twax.set_xlabel('ice volume (m sea level equivalent)')

    # remove spines
    tsax.spines['left'].set_visible(False)
    tsax.spines['right'].set_visible(False)
    twax.spines['left'].set_visible(False)
    twax.spines['right'].set_visible(False)

    # add cursor
    tsax.axhline(-time/1e3, c='0.25', lw=0.5)
    tsax.set_yticks([120, -time/1e3, 0.1])  # mpl confused with two 0 ticks
    tsax.set_yticklabels([
        r'120$\,$000' if time >= -110000 else '',
        '{:,d}\nyears ago'.format(-time).replace(',', r'$\,$'),
        '0' if time <= -10000 else ''])

    # return figure
    return fig


def main():
    """Main program for command-line execution."""

    # start and end of animation
    start, end, step = -120000, -0, 5000

    # output frame directories
    outdir = os.path.join(os.environ['HOME'], 'anim', 'anim_cordillera_dual')

    # iterable arguments to save animation frames
    iter_args = [(draw, outdir, t) for t in range(start+step, end+1, step)]

    # create frame directory if missing
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # plot all frames in parallel
    with mp.Pool(processes=4) as pool:
        pool.starmap(save_animation_frame, iter_args)


if __name__ == '__main__':
    main()
