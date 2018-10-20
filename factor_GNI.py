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
data = pd.read_csv('data_miraibadpackets_all.csv', sep=';', na_filter = False)

# remove all rows for which we don't know the ISP or the GNI
data2 = data[data.isp != "NULL"]
data2 = data[data.isp != '']
data2 = data2[data2.GNI_pc_2017 != '']
# list all remaining isps
isps = list(set(data2['isp']))

# count occurrences per isp and store the GNI of their country
infections = list()
ispGNI = list()
for isp in isps:
    ispData = data2[data2.isp == isp]
    gni = op_names[op_names.op == isp]['GNI_pc_2017']
    # only add if we have data on it
    if len(gni) != 0:
        ispGNI.append(list(gni)[0])
        infections.append(len(ispData))
    
#ispGNI = list(map(int, ispGNI))

plt.scatter(ispGNI, infections, marker='.')
slope, intercept, r_value, p_value, std_err = stats.linregress(ispGNI,infections)
line = [slope*i+intercept for i in ispGNI]
plt.plot(ispGNI,line, color='red', label="regression line")
# zoom in a bit
plt.ylim(bottom=-500)
plt.xlim(left=0)
plt.xlabel("GNI in $ per capita in ISP country of origin (2017)")
plt.ylabel("Total new infections observed")
plt.legend(bbox_to_anchor=(1, 1))
plt.savefig("images/block4/factor_gni.png")
plt.clf()

plt.scatter(ispGNI, infections, marker='.')
slope, intercept, r_value, p_value, std_err = stats.linregress(ispGNI,infections)
line = [slope*i+intercept for i in ispGNI]
plt.plot(ispGNI,line, color='red', label="regression line")
# zoom in a bit
plt.ylim(bottom=-25, top=2000)
plt.xlim(left=0)
plt.xlabel("GNI in $ per capita in ISP country of origin (2017)")
plt.ylabel("Total new infections observed")
plt.legend(bbox_to_anchor=(1, 1))
plt.savefig("images/block4/factor_gni_zoomed.png")
plt.clf()

print("Pearson's correlation coefficient: {0:.4f}".format(pearsonr(ispGNI,infections)[0]))
print("P-value: {0:.4f}".format(pearsonr(ispGNI,infections)[1]))
