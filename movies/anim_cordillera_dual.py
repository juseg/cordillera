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
import cartowik.conventions as ccv
import cartowik.decorations as cde
import cartowik.naturalearth as cne
import cartowik.shadedrelief as csr
import absplots as apl
import pismx.open


# Color palette
# -------------

# set color cycle to colorbrewer Paired palette
plt.rc('axes', prop_cycle=plt.cycler(color=plt.get_cmap('Paired').colors))


# Plotting methods
# ----------------

def draw_natural_earth(ax, mode='gs'):
    """Add Natural Earth geographic data vectors."""
    edgecolor = '#0978ab' if mode == 'co' else '0.25'
    facecolor = '#c6ecff' if mode == 'co' else '0.95'
    kwargs = dict(ax=ax, scale='50m', zorder=0)
    cne.add_rivers(edgecolor=edgecolor, **kwargs)
    cne.add_lakes(edgecolor=edgecolor, facecolor=facecolor, **kwargs)
    cne.add_coastline(edgecolor=edgecolor, linestyle='dashed', **kwargs)


def plot_visual(ax, run, time, mode='gs'):
    """Plot interpolated map-plane model output."""

    # get interpolated sea level
    with pismx.open.dataset('~/pism/input/dsl/specmap.nc') as ds:
        dsl = ds.delta_SL.interp(age=-time/1e3, method='linear')

    # plot interpolated model output
    with pismx.open.visual(
            run+'/ex.{:07.0f}.nc',
            '~/pism/input/boot/cordillera.etopo1bed.hus12.5km.nc',
            '~/pism/input/boot/cordillera.etopo1bed.hus12.1km.nc',
            ax=ax, time=time, shift=120000) as ds:
        ds.topg.plot.imshow(
            ax=ax, add_colorbar=False, zorder=-1,
            cmap=(ccv.ELEVATIONAL if mode == 'co' else 'Greys'),
            vmin=(-4500 if mode == 'co' else 0), vmax=4500)
        csr.add_multishade(
            ds.topg.where(ds.topg >= dsl)-dsl,
            ax=ax, add_colorbar=False, zorder=-1)
        ds.topg.plot.contour(
            ax=ax, colors=('#0978ab' if mode == 'co' else '0.25'),
            levels=[dsl], linestyles='solid', linewidths=0.25, zorder=0)
        ds.usurf.plot.contour(
            levels=[lev for lev in range(0, 5000, 200) if lev % 1000 == 0],
            ax=ax, colors=['0.25'], linewidths=0.25)
        ds.usurf.plot.contour(
            levels=[lev for lev in range(0, 5000, 200) if lev % 1000 != 0],
            ax=ax, colors=['0.25'], linewidths=0.1)
        ds.velsurf_mag.notnull().plot.contour(
            ax=ax, colors=['0.25'], levels=[0.5], linewidths=0.25)
        mappable = ds.velsurf_mag.plot.imshow(
            ax=ax, add_colorbar=False, cmap='Blues',
            norm=mcolors.LogNorm(1e1, 1e3), alpha=0.75)

    # return mappable for unique colorbar
    return mappable


def plot_series(tsax, twax, run, time):
    """Plot model output time series."""

    rec = run.split('.')[-2].upper()
    dtfile = '.3222.'.join(run.split('.')[-2:])
    color = 'C1' if 'grip' in run else 'C5'

    # plot temperature forcing
    with pismx.open.dataset('~/pism/input/dt/'+dtfile+'.nc') as ds:
        data = ds.delta_T[ds.time <= time]
        tsax.plot(data, data.age, color=color, alpha=0.25)
        tsax.text(data[-1], -time/1e3, '{:.1f}°C'.format(float(data[-1])),
                  ha='center', va='bottom', clip_on=True, color=color,
                  alpha=0.25)

    # plot ice volume time series
    with pismx.open.mfdataset(run+'/ts.???????.nc') as ds:
        data = ds.slvol[ds.age >= -time/1e3]
        twax.plot(data, data.age, color=color, label=rec)
        twax.text(data[-1], -time/1e3, '{:.1f} m'.format(float(data[-1])),
                  ha='center', va='bottom', clip_on=True, color=color)


def draw(time):
    """Plot complete figure for given time."""

    # initialize figure (108*1500/2700=60)
    fig, grid = apl.subplots_mm(
        ncols=2, nrows=1, sharex=True, sharey=True, figsize=(192, 108),
        gridspec_kw=dict(left=0, right=0, bottom=0, top=0, wspace=192-135),
        subplot_kw=dict(projection=ccrs.LambertConformal(
            central_longitude=-95, central_latitude=49,
            standard_parallels=(49, 77))))
    cax = fig.add_axes_mm([135/2+10, 108-10, 192-135-20, 5])
    tsax = fig.add_axes_mm([135/2+5, 10, 192-135-20, 108-40])
    twax = tsax.twiny()

    # prepare map axes
    for i, ax in enumerate(grid):
        ax.set_extent([-2500e3, -1000e3, 100e3, 2500e3], crs=ax.projection)
        ax.spines['geo'].set_ec('none')
        ax.plot([1-i, 1-i], [0, 1], transform=ax.transAxes, color='k', lw=2)

    # for each record
    for i, rec in enumerate(['GRIP', 'EPICA']):
        ax = grid[i]
        offset = [6.2, 5.9][i]
        run = '~/pism/output/0.7.2-craypetsc/ciscyc4.5km.{:s}.{:04d}'
        run = run.format(rec.lower(), round(offset*100))

        # plot model output
        mappable = plot_visual(ax, run, time)
        plot_series(tsax, twax, run, time)

        # add map elements
        draw_natural_earth(ax)
        cde.add_subfig_label(rec, ax=ax, loc='ne')

    # add unique colorbar
    fig.colorbar(mappable, cax=cax, format='%g', orientation='horizontal',
                 label=r'surface velocity ($m\,a^{-1}$)', extend='both')

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

    # legend appears after a bit
    if time >= -105000:
        twax.legend(loc='lower right')

    # remove spines
    tsax.spines['left'].set_visible(False)
    tsax.spines['right'].set_visible(False)
    twax.spines['left'].set_visible(False)
    twax.spines['right'].set_visible(False)

    # add cursor
    tsax.axhline(-time/1e3, c='0.25', lw=0.5)
    tsax.set_yticks([120, -(time+1)/1e3, 0])  # mpl confused with two 0 ticks
    tsax.set_yticklabels([
        r'120$\,$000' if time >= -110000 else '',
        '{:,d}\nyears ago'.format(-time).replace(',', r'$\,$'),
        '0' if time <= -10000 else ''])

    # return figure
    return fig


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


# Main program
# ------------

def main():
    """Main program for command-line execution."""

    # start and end of animation
    start, end, step = -120000, -0, 100

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
