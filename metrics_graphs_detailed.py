import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime as dt
from datetime import datetime
from datetime import timedelta

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# import data and convert to datetime
data = pd.read_csv('data_miraibadpackets.csv', sep=';', na_filter = False)
ips_per_country = pd.read_csv('total_ips_per_country.csv',na_filter = False)
dfs = data['Date_First_Seen']
dfs = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dfs]

# create bins of 2 weeks each, for unique countries/AS graphs
metric = list()
d = timedelta(3) # 14 days
start = datetime.combine(dt.date(2018,4,28),datetime.min.time())
end = datetime.combine(dt.date(2018,8,1),datetime.min.time())

bins = 1
totalInfCount = 0
countries = set()
autsys = set()
binstart = start
c = len(dfs)
while c > 0:
    c = c-1
    if dfs[c] - binstart > d:
        metric.append([binstart,totalInfCount,len(countries),len(autsys)])
        bins = bins + 1
        binstart = dfs[c]
        totalInfCount = 0
        countries = set()
        autsys = set()
    totalInfCount = totalInfCount + 1
    countries.add(data['Country'][c])
    autsys.add(data['ASN'][c])
    #display progress
    if c % 10 == 0:
        print "{0:.1f}%".format((len(dfs)-c)/float(len(dfs))*100)
        sys.stdout.write("\033[F")

metric.append([binstart,totalInfCount,len(countries),len(autsys)])
metric = metric[1:]
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
plt.ylabel("amount of new infections in dataset")
plt.savefig('images/metric_total_infections_detailed.png')
plt.gcf().clear()

plt.bar(range(0,len(metric)), [m[2] for m in metric])
plt.xticks(range(-1,len(metric)-1,5), labels, rotation=50, fontsize=8)
plt.xlabel("time: bin size of 14 days")
plt.ylabel("number of unique countries")
plt.savefig('images/metric_unique_countries_detailed.png')
plt.gcf().clear()

plt.bar(range(0,len(metric)), [m[3] for m in metric])
plt.xticks(range(-1,len(metric)-1,5), labels, rotation=50, fontsize=8)
plt.xlabel("time: bin size of 14 days")
plt.ylabel("number of unique Autonomous Systems")
plt.savefig('images/metric_unique_as_detailed.png')
plt.gcf().clear()


