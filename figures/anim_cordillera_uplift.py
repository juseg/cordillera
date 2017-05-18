#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
from matplotlib.animation import FuncAnimation

# uplift contour levels and colors
levs = [-600.0, -400.0, -200.0, 0.0, 10.0, 20.0, 30.0]
cmap = ut.pl.get_cmap('RdBu_r', len(levs)+1)
cols = cmap(range(len(levs)+1))

# drawing function
def draw(t, grid, tsax, twax):
    """What to draw at each animation step."""
    a = -t/1e3
    print 'plotting at %.1f ka...' % a

    # clear time series axes
    tsax.cla()
    twax.cla()

    # for each record
    for i, rec in enumerate(ut.cisbed_records):
        c = ut.cisbed_colours[i]
        dt = ut.cisbed_offsets[i]
        dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))
        run_dir = 'output/e9d2d1f/cordillera-narr-10km/%s+cisbed1+till1545' % dt_file

        # load ice volume time series
        nc = ut.io.load(run_dir + '/y???????-ts.nc')
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)
        vol = nc.variables['slvol'][:]
        nc.close()

        # plot ice volume time series
        tsax.plot(vol[age>=a], age[age>=a], color='0.25')

        # load bedrock topography
        nc = ut.io.load(run_dir + '/y???????-extra.nc')
        x = nc.variables['x'][:]
        y = nc.variables['y'][:]
        z = nc.variables['topg'][:]
        age = -nc.variables['time'][:]/(1e3*365*24*60*60)

        # plot bedrock depression time series
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        dep = (zref-z).sum(axis=(1, 2))*dx*dy*1e-12
        twax.plot(dep[age>=a], age[age>=a], c=c)

        # clear map axes
        ax = grid[i]
        ax.cla()
        ax.outline_patch.set_ec('none')
        ax.set_extent(ut.pl.regions['cordillera'], crs=ax.projection)

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
        nc.close()

        # add map elements
        ut.pl.draw_natural_earth(ax)
        ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (rec, a))

    # set time series axes properties
    tsax.set_ylim(120.0, 0.0)
    tsax.set_xlim(9.5, -0.5)
    tsax.set_ylabel('age (ka)')
    tsax.set_xlabel('ice volume (m s.l.e.)', color='0.25')
    tsax.yaxis.tick_right()
    tsax.yaxis.set_label_position('right')
    tsax.grid(axis='x')

    # set twin axes properties
    twax.set_xlim(950.0, -50.0)
    twax.set_xlabel('volumic depression ($10^{3}\,km^{3}$)')

    # return mappable for colorbar
    return im

# initialize figure
fig, grid, cax, tsax = ut.pl.subplots_2_cax_ts_anim()
twax = tsax.twiny()

# add signature
figw, figh = [dim*25.4 for dim in fig.get_size_inches()]
fig.text(1-2.5/figw, 2.5/figh, 'J. Seguinot et al. (in prep.)',
         ha='right', va='bottom')

# load boot topo
filepath = 'input/boot/cordillera-etopo1bed+thk+gou11simi-10km.nc'
nc = ut.io.load(filepath)
zref = nc.variables['topg'][:].T
nc.close()

# draw first frame and colorbar
im = draw(-60e3, grid, tsax, twax)
cb = fig.colorbar(im, cax, orientation='horizontal')
cb.set_label('bedrock uplift (m)')

# save preview
ut.pl.savefig(fig)

# make animation
frames = -np.arange(0e3, 120e3, 100.0)[::-1]
anim = FuncAnimation(fig, draw, frames=frames, fargs=(grid, tsax, twax))
anim.save('anim_cordillera_uplift.mp4', fps=25, codec='h264')
anim.save('anim_cordillera_uplift.ogg', fps=25, codec='theora')
