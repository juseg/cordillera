#!/usr/bin/env python2
# coding: utf-8

"""Parameters for low-resolution runs."""

records = ['grip', 'ngrip', 'epica', 'vostok', 'odp1012', 'odp1020']
labels = ['GRIP', 'NGRIP', 'EPICA', 'Vostok', 'ODP 1012', 'ODP 1020']
colors = ['#1F78B4', '#A6CEE3', '#E31A1C', '#FB9A99', '#33A02C', '#B2DF8A']
markers = ['s', 'D', 'o', 'h', 'v', '^']
offsets = [6.2, 6.6, 5.9, 5.95, 6.15, 6.05]

# 32 to 22 ka offsets before scaling
noscale = [-16.4126, -26.7098, -9.2055, -7.9550, -3.7889, -5.0000]