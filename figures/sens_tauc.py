#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np
import iceplotlib.plot as iplt


def tillphi(b, phi_0=15.0, phi_1=45.0, b_0=0.0, b_1=200.0):
    """Return till friction angle as a function of elevation."""
    phi = phi_0 + (phi_1-phi_0) * (b-b_0) / (b_1-b_0)
    phi = np.clip(phi, phi_0, phi_1)
    return phi


def tauc_min(phi,
             c0=0.0,
             ax=None,
             delta=0.02,  # -      (Bueler and van Pelt, 2015)
             h=1000.0,    # m      (Bueler and van Pelt, 2015)
             rho=910.0,   # kg m-3 (Bueler and van Pelt, 2015)
             g=9.81,      # m s-2  (Bueler and van Pelt, 2015)
             ):
    """Return minimum yield stress, corresponding to saturated till, as a
    function of till friction angle."""
    Ntil_min = delta * rho * g * h
    tauc_min = c0 + Ntil_min * phi
    return tauc_min


if __name__ == '__main__':

    # bed elevation
    b = np.linspace(-200.0, 400.0, 101)

    # initialize figure
    fig, ax = iplt.subplots_mm(1, 1, sharex=True, figsize=(85.0, 60.0),
                                 left=10.0, right=2.5, bottom=10.0, top=2.5,
                                 wspace=2.5, hspace=2.5)

    # plot default run
    ax.plot(b, tauc_min(tillphi(b))*1e-5, 'k')

    # plot with different friction angles
    ax.plot(b, tauc_min(tillphi(b, 24.0, 24.0))*1e-5, c='k', ls='--')

    # plot with different delta
    for delta in [0.01, 0.05]:
        ax.plot(b, tauc_min(tillphi(b), delta=delta)*1e-5, c=ut.colors[2])

    # set axes properties
    ax.set_xlabel('b (m)')
    ax.set_ylabel(r'$\tau_{c,min}$ (bar)')
    ax.grid()
    
    # save
    fig.savefig('sens_tauc')
