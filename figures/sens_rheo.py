#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt
from matplotlib.ticker import FuncFormatter

def A_bb09(T,
           A_cold=3.61e-13,  # Pa-3 s-1    (Bueler and Brown, 2009)
           A_warm=1.73e+03,  # Pa-3 s-1    (Bueler and Brown, 2009)
           Q_cold=6e4,       # J mol-1     (Bueler and Brown, 2009)
           Q_warm=139e3,     # J mol-1     (Bueler and Brown, 2009)
           T_star=263.15,    # K           (Bueler and Brown, 2009)
           R=8.314,          # J mol-1 K-1 (Bueler and Brown, 2009)
           ):
    """Return creep parameter A for given temperature vector T
    using Bueler and Brown (2009) four-parameter formulation.
    Default parameters are from Bueler and Brown (2009).
    """
    A = np.where(T < T_star,
                 A_cold * np.exp(-Q_cold/R/T),
                 A_warm * np.exp(-Q_warm/R/T))
    return A


def A_cp10(T,
           A_star=3.5e-25,   # Pa-3 s-1    (Cuffey and Paterson, 2010, p. 76)
           Q_cold=6e4,       # J mol-1     (Cuffey and Paterson, 2010, p. 72)
           Q_warm=115e3,     # J mol-1     (Cuffey and Paterson, 2010, p. 76)
           T_star=263.15,    # K           (Cuffey and Paterson, 2010, p. 72)
           R=8.314,          # J mol-1 K-1 (Cuffey and Paterson, 2010, p. 72)
           ):
    """Return creep parameter A for given temperature vector T
    using Cuffey and Paterson (2010) three-parameter formulation.
    Default parameters are from Cuffey and Paterson (2010).
    """
    Q = np.where(T < T_star, Q_cold, Q_warm)
    A = A_star * np.exp(-Q/R*(1/T-1/T_star))
    return A


if __name__ == '__main__':

    # pressure-adjusted temperature
    T = np.linspace(253.15, 273.15, 101)

    # initialize figure
    fig, grid = iplt.subplots_mm(2, 1, sharex=True, figsize=(85.0, 100.0),
                                 left=10.0, right=2.5, bottom=7.5, top=2.5,
                                 wspace=2.5, hspace=2.5)

    # for each axes
    for ax in grid:

        # plot softness as in Bueler and Brown, 2009
        A = A_bb09(T)
        ax.plot(T-273.15, A, c=ut.colors[2], label='Paterson and Budd, 1982')

        # plot softness as in Cuffey and Paterson, 2010
        A = A_cp10(T)
        ax.plot(T-273.15, A, c=ut.colors[0], label='Cuffey and Paterson, 2010')
        ax.plot(T-273.15, 2*A, c=ut.colors[0], ls='--')
        ax.plot(T-273.15, 5*A, c=ut.colors[0], ls='--')

        # set axes properties
        ax.grid()

    # linear scale on top axes
    grid[0].legend(loc='best')
    ticks = FuncFormatter(lambda x, pos: '{0:g}'.format(x*1e24))
    ticks = FuncFormatter(lambda x, pos: '%g' % (x*1e24))
    grid[0].yaxis.set_major_formatter(ticks)
    grid[0].text(-0.125, 0.5, r'ice softness $A$ ($10^{-24}\,Pa^{-3}\,s^{-1}$)',
                 va='center', rotation=90.0, transform=grid[0].transAxes)

    # log scale on bottom axes
    grid[1].set_xlabel(u'temparture $T$ (°C)')
    grid[1].set_yscale('log')
    grid[1].text(-0.125, 0.5, r'ice softness $A$ ($Pa^{-3}\,s^{-1}$)',
                 va='center', rotation=90.0, transform=grid[1].transAxes)
    
    # save
    fig.savefig('sens-rheo')
