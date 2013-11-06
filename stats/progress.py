#!/usr/bin/env python2

#import csv
#dates = []
#words = []
#with open('count.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         dates.append(row[0])
#         words.append(row[1])

from matplotlib import pyplot as plt
plt.plotfile('count.csv', (0,1), plotfuncs={1:'step'})
#plt.show()
plt.savefig('progress.pdf')
