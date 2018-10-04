import pandas as pd
import matplotlib as mat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import sys

# import data, parse to datetime, and reverse so we don't go back in time 
data = pd.read_csv('data_maraibadpackets_isp.csv', sep=';', na_filter = False)
data['Date_First_Seen'] = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in data['Date_First_Seen']]
data = data.reindex(index=data.index[::-1])

# remove all rows for which we don't know the ISP
data2 = data[data.isp != "NULL"]

isps = set(data2['isp'])

# for now simply count them without normalizing
counts = list()
valueCounts = data2.isp.value_counts()
for isp in isps:
    counts.append(valueCounts[isp])

ispCount = pd.DataFrame({'isp' : list(isps), 'count' : counts})
ispCount = ispCount.sort_values(by=['count'])

# plot a few isps
isp0 = data2[data2.isp == ispCount['isp'][0]].reset_index(drop=True)
isp1 = data2[data2.isp == ispCount['isp'][(len(ispCount)-1)/4]].reset_index(drop=True)
isp2 = data2[data2.isp == ispCount['isp'][(len(ispCount)-1)/2]].reset_index(drop=True)
isp3 = data2[data2.isp == ispCount['isp'][3*(len(ispCount)-1)/4]].reset_index(drop=True)
isp4 = data2[data2.isp == ispCount['isp'][len(ispCount)-1]].reset_index(drop=True)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

plt.plot(isp0['Date_First_Seen'], range(0,ispCount['count'][0]), label=isp0['isp'][0])
plt.plot(isp1['Date_First_Seen'], range(0,ispCount['count'][(len(ispCount)-1)/4]), label=isp1['isp'][0])
plt.plot(isp2['Date_First_Seen'], range(0,ispCount['count'][(len(ispCount)-1)/2]), label=isp2['isp'][0])
plt.plot(isp3['Date_First_Seen'], range(0,ispCount['count'][3*(len(ispCount)-1)/4]), label=isp3['isp'][0])
plt.plot(isp4['Date_First_Seen'], range(0,ispCount['count'][len(ispCount)-1]), label=isp4['isp'][0])


plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.show()
