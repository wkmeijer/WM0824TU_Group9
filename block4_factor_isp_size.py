import pandas as pd
import matplotlib as mat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy import stats
from datetime import datetime
from scipy.stats.stats import pearsonr
from numpy.polynomial.polynomial import polyfit
import statsmodels.api as sm
import sys

op_names = pd.read_csv('op_names_v2.csv', na_filter = False)
data = pd.read_csv('data_maraibadpackets_isp.csv', sep=';', na_filter = False)

# remove all rows for which we don't know the ISP
data2 = data[data.isp != "NULL"]

isps = set(data2['isp'])

# for now simply count them without normalizing
counts = list()
valueCounts = data2.isp.value_counts()
for isp in isps:
    counts.append(valueCounts[isp])

ispCount = pd.DataFrame({'isp' : list(isps), 'count' : counts})
ispCount = ispCount.reindex(index=ispCount.index[::-1])

infections = list()
sizes = list()

# skip all ISP's for which we don't know their size
for i in range(len(ispCount)-1):
    size = op_names[op_names.op == ispCount['isp'][i]]['size']
    if len(size) != 0 and list(size)[0] != 0:
        infections.append(ispCount['count'][i])
        sizes.append(list(size)[0])

plt.scatter(sizes, infections, marker='.')
#b, m = polyfit(sizes, infections, 1)
#plt.plot(sizes, [b + m *float(s) for s in sizes], '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(sizes,infections)
line = [slope*s+intercept for s in sizes]
plt.plot(sizes,line, color='red')
# zoom in a bit
plt.ylim(top=9000, bottom=0)
plt.xlim(right=120000000, left=0)
plt.xlabel("ISP size")
plt.ylabel("Total new infections observed")
plt.savefig("images/block4/factor_isp_size_zoomed.png")
plt.clf()

print("Pearson's correlation coefficient: {0:.4f}".format(pearsonr(sizes,infections)[0]))
print("P-value: {0:.4f}".format(pearsonr(sizes,infections)[1]))

