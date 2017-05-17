#!/usr/bin/env python2
# coding: utf-8

import util as ut
from matplotlib.animation import FuncAnimation

# uplift contour levels and colors
levs = [-600.0, -400.0, -200.0, 0.0, 10.0, 20.0, 30.0]
cmap = ut.pl.get_cmap('RdBu_r', len(levs)+1)
cols = cmap(range(len(levs)+1))

# drawing function
def draw(t, grid, cursor):
    """What to draw at each animation step."""
    age = -t/1e3
    print 'plotting at %.1f ka...' % age

    # update cursor
    cursor.set_data([0, 1], [age, age])

    # plot maps
    for i, rec in enumerate(ut.cisbed_records):
        dt = ut.cisbed_offsets[i]
        ax = grid[i]
        ax.cla()
        ax.outline_patch.set_ec('none')
        ax.set_extent(ut.pl.regions['cordillera'], crs=ax.projection)
        dt_file = '%s3222cool%04d' % (rec.lower(), round(dt*100))
        nc = ut.io.load('output/e9d2d1f/cordillera-narr-10km/'
                        '%s+cisbed1+till1545/y???????-extra.nc' % dt_file)
        x, y, z = nc._extract_xyz('topg', t)
        im = nc.imshow('topg', ax, t, vmin=0.0, vmax=3e3, cmap='Greys', zorder=-1)
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
        ut.pl.add_corner_tag(ax, '%s, %.1f ka' % (rec, age))

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
    tsax.plot(vol, age, color='0.25')

    # load bedrock topography
    nc = ut.io.load(run_dir + '/y???????-extra.nc')
    x = nc.variables['x'][:]
    y = nc.variables['y'][:]
    z = nc.variables['topg'][:]
    time = nc.variables['time'][:]/(365*24*60*60)
    nc.close()

    # plot bedrock depression
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    z = (zref-z).sum(axis=(1, 2))*dx*dy*1e-12
    twax.plot(z, -time/1e3, c=c)

# set time series axes properties
tsax.set_ylim(120.0, 0.0)
tsax.set_xlim(9.5, -0.5)
tsax.set_ylabel('age (ka)')
tsax.set_xlabel('ice volume (m s.l.e.)', color='0.25')
tsax.grid(axis='x')

# set twin axes properties
twax.grid(axis='y')
twax.set_xlim(950.0, -50.0)
twax.set_xlabel('volumic depression ($10^{3}\,km^{3}$)')
twax.grid(axis='x')

# init moving cursor
cursor = tsax.axhline(60.0, c='k', lw=0.25)

# draw first frame and colorbar
im = draw(0, grid, cursor)
cb = fig.colorbar(im, cax, orientation='horizontal')
cb.set_label('bedrock uplift (m)')

# make animation
#ut.pl.savefig(fig)
anim = FuncAnimation(fig, draw, frames=time, fargs=(grid, cursor))
anim.save('anim_cordillera_uplift.mp4', fps=25, codec='h264')
anim.save('anim_cordillera_uplift.ogg', fps=25, codec='theora')
