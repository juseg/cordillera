#!/usr/bin/env python2
# coding: utf-8

from matplotlib import pyplot as plt
plt.plotfile('count.csv', (0, 1), plotfuncs={1:'step'})
plt.savefig('progress.pdf')
