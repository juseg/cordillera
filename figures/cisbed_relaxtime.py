#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np

# initialize figure
fig, ax = ut.pl.subplots_ts()

# parameters
D = 2.4e+24  # lithosphere flexural rigidity for 60km elastic thickness
rho = 3300.0  # mantle density
nu = 1e19  # mantle viscosity
g = 9.81  # standard gravity
pi = np.pi

# for two different viscosities
for nu in [1e21, 1e19]:

    # compute response time
    lam = np.logspace(5, 8, 101)
    tau = 4*pi*nu*lam**-1 / (rho*g + 16*pi**4*D*lam**-4)
    tau /= (365*24*60*60)

    # plot
    label = r'$\nu_m={}$'.format(nu)
    ax.plot(lam/1e3, tau, label=label)

# set axes properties
ax.set_xlabel('wavelength (km)')
ax.set_ylabel('relaxation time (a)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()

# save
ut.pl.savefig(fig)
