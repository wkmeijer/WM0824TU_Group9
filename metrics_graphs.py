import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime
from datetime import timedelta

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# import data and convert to datetime
data = pd.read_csv('data_miraibadpackets.csv', sep=';')
dfs = data['Date_First_Seen']
dfs = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dfs]

# create bins of 2 weeks each
metric = list()
d = timedelta(14) # 14 days
start = dfs[len(dfs)-1]
end = dfs[0]

bins = 1
countries = set()
autsys = set()
binstart = start
c = len(dfs)
while c > 0:
    c = c-1
    if dfs[c] - binstart > d:
        metric.append([binstart,len(countries),len(autsys)])
        bins = bins + 1
        binstart = dfs[c]
        countries = set()
        autsys = set()
    countries.add(data['Country'][c])
    autsys.add(data['ASN'][c])
    #display progress
    if c % 10 == 0:
        print "{0:.1f}%".format((len(dfs)-c)/float(len(dfs))*100)
        sys.stdout.write("\033[F")

metric.append([binstart,len(countries),len(autsys)])
print "100.0%"

# create labels every 5 bars
date = start
labels = list()
while date < dfs[0]:
    labels.append(str(date.date()))
    date = date + 5*d

plt.bar(range(0,len(metric)), [m[1] for m in metric])
plt.xticks(range(-1,len(metric)-1,5), labels, rotation=50, fontsize=8)
plt.xlabel("time: bin size of 14 days")
plt.ylabel("number of unique countries")
plt.savefig('images/metric_unique_countries.png')

plt.bar(range(0,len(metric)), [m[2] for m in metric])
plt.xticks(range(-1,len(metric)-1,5), labels, rotation=50, fontsize=8)
plt.xlabel("time: bin size of 14 days")
plt.ylabel("number of unique Autonomous Systems")
plt.savefig('images/metric_unique_as.png')
