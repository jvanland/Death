#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from definitions import *

passfile = '/Users/johnnyvanlandingham/Documents/DataScience/password.txt'

group = 'year'
filter_type = 'sex'
table = query(passfile,group,filter_type,0)

N = 21
mdeaths = N*[0]
fdeaths = N*[0]
for j in range(N):
    mdeaths[j] = 10000*table[1][j]/table[3][j]
    fdeaths[j] = 10000*table[2][j]/table[3][j]

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()

men = ax.bar(ind, mdeaths, width, color='r')
women = ax.bar(ind + width, fdeaths, width, color='g')

ax.set_ylabel('Deaths per 10,000 people')
ax.set_title('Mortality')
ax.set_xticks(ind + width)
ax.set_xticklabels(table[0])

ax.legend((men[0], women[0]), ('Men', 'Women'))

plt.show()

