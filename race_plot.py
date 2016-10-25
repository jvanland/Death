#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from definitions import *

passfile = '/Users/johnnyvanlandingham/Documents/DataScience/password.txt'

group = 'year'
filter_type = 'race'
table = query(passfile,group,filter_type,0)

N = 21
wdeaths = N*[0]
bdeaths = N*[0]
odeaths = N*[0]
for j in range(N):
    wdeaths[j] = 10000*table[2][j]/table[1][j]
    bdeaths[j] = 10000*table[3][j]/table[1][j]
    odeaths[j] = 10000*table[4][j]/table[1][j]

ind = np.arange(N)  # the x locations for the groups
width = 0.25       # the width of the bars

fig, ax = plt.subplots()

white = ax.bar(ind, wdeaths, width, color='r')
black = ax.bar(ind+width, bdeaths, width, color='g')
other = ax.bar(ind+width+width, odeaths, width, color='b')

ax.set_ylabel('Deaths per 10,000 people')
ax.set_title('Mortality')
ax.set_xticks(ind + width)
ax.set_xticklabels(table[0])

ax.legend((white[0], black[0], other[0]), ('White', 'Black', 'Other'))

plt.show()
