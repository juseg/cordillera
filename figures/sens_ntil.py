#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.transforms import ScaledTranslation

def plot_Ntil(W,
              ax=None,
              delta=0.02,  # -      (Bueler and van Pelt, 2015)
              Wmax=2.0,    # m      (Bueler and van Pelt, 2015)
              h=1000.0,    # m      (Bueler and van Pelt, 2015)
              e0=0.69,     # -      (Bueler and van Pelt, 2015)
              Cc=0.12,     # -      (Bueler and van Pelt, 2015)
              rho=910.0,   # kg m-3 (Bueler and van Pelt, 2015)
              g=9.81,      # m s-2  (Bueler and van Pelt, 2015)
              annotate=False,
              **kwargs):
    """Plot effective pressure on till as a function of water level in the
    style of Bueler and van Pelt (2015, Fig. 1).
    Default parameters are from Bueler and van Pelt (2015, Table 1)."""
    
    # get current axes if None is given
    ax = ax or iplt.gca()

    # compute bound and unbound Ntil
    P0 = rho * g * h
    Ntil_cap = delta * P0 * 10**(e0/Cc*(1-(W/Wmax)))
    Ntil = np.minimum(P0, Ntil_cap)
    Ntil_cap = np.ma.array(Ntil, mask=(W<Wmax))
    Ntil = np.ma.array(Ntil, mask=(W>Wmax))
    
    # plot in bars
    ax.plot(W, Ntil_cap*1e-5, ls=':', **kwargs)
    ax.plot(W, Ntil*1e-5, ls='-', **kwargs)
    ax.plot(Wmax, delta*P0*1e-5, marker='o', **kwargs)

    # add annotations
    if annotate is True:

        # prepare offset transform
        transOffset = ScaledTranslation(2.0/72, 2.0/72,
                                        ax.figure.dpi_scale_trans)

        # compute point of compensation where Ntil_cap = P0
        W0 = Wmax * (1+Cc/e0*np.log10(delta))

        # mark point of compensation
        ax.text(W0, P0*1e-5, '$W_0, P_0$',
                transform=ax.transData+transOffset, **kwargs)

        # mark minimal effective pressure
        ax.text(Wmax, delta*P0*1e-5, '$W_{max}, \delta P_0$',
                transform=ax.transData+transOffset,**kwargs)


if __name__ == '__main__':

    # pressure-adjusted temperature
    W = np.linspace(0.0, 6.0, 121)

    # initialize figure
    fig, grid = iplt.subplots_mm(nrows=2, ncols=1, sharex=True, figsize=(85.0, 100.0),
                                 left=10.0, right=2.5, bottom=10.0, top=2.5,
                                 wspace=2.5, hspace=2.5)

    # for each axes
    for ax in grid:

        # plot default run
        plot_Ntil(W, ax=ax, color='k')

        # plot with different Wmax
        plot_Ntil(W, ax=ax, Wmax=1.0, color=ut.colors[0])
        plot_Ntil(W, ax=ax, Wmax=5.0, color=ut.colors[0], annotate=True)

        # plot with different delta
        plot_Ntil(W, ax=ax, delta=0.01, color=ut.colors[2])
        plot_Ntil(W, ax=ax, delta=0.05, color=ut.colors[2])

        # set axes properties
        ax.set_ylabel('Ntil (bar)')
        ax.grid()

    # linear scale on top axes
    grid[0].set_ylim(-2.0, 100.0)

    # log scale on bottom axes
    grid[1].set_xlabel('W (m)')
    grid[1].set_ylim(2e-1, 2e2)
    grid[1].set_yscale('log')

    # save
    fig.savefig('sens_ntil')
