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
ispCount = ispCount.reindex(index=ispCount.index[::-1])

# plot a few isps, the indices are random numbers generated earlier to keep the same picture each time the script is run
indices = [74,22,148,176,141,18,223,90,229,221,32,230,76,62]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for i in indices:
    ispData = data2[data2.isp == ispCount['isp'][i]].reset_index(drop=True)
    plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispData['isp'][0])

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/selection_of_isps.png")
plt.clf()


# plot data of same global company (tele 2)
tele2 = ['AT01','DE09', 'DK02', 'NL04', 'SE02']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in tele2:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 0:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/tele2_global.png")
plt.clf()


# plot data of same global company (vodafone)
vodafone = ['CZ06', 'DE01', 'EG03', 'ES06', 'GB10', 'IE09', 'IS02', 'IT05', 'MT03', 'NL08', 'NZ03', 'PT05', 'RO08', 'TR06']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in vodafone:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 0:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/vodafone_global.png")
plt.clf()


# plot data of same global company (orange)
orange = ['ES04','FR02', 'GB07', 'LU02', 'PL09', 'RO07', 'SK01']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in orange:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 0:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/orange_global.png")
plt.clf()

# plot data of continents
europe = ['AT01','AT02','AT03','BE01','BE02','BE03','BE04','BG01','BG02','BG03','BG04','BG05','BG06','BY01','BY02','BY03','CH01','CH02','CH03','CH05','CY01','CY02','CY03','CY04','CZ01','CZ02','CZ03','CZ04','CZ05','CZ06','DE01','DE02','DE07','DE08','DE09','DE10','DE11','DE12','DE13','DK01','DK02','DK03','DK04','EE01','EE02','EE03','ES01','ES02','ES03','ES04','ES05','ES06','FI01','FI02','FI03','FI05','FR01','FR02','FR03','FR05','FR06','GB01','GB02','GB04','GB05','GB07','GB09','GB10','GR01','GR02','GR03','GR04','GR05','HR03','HR04','HR05','HU02','HU03','HU04','HU05','HU06','IE02','IE03','IE04','IE05','IE08','IE09','IE10','IS01','IS02','IS03','IS04','IT01','IT02','IT03','IT04','IT05','LT01','LT02','LT04','LT05','LU01','LU02','LV01','LV02','LV03','LV05','MT01','MT02','MT03','NL02','NL03','NL04','NL05','NL06','NL07','NL08','NO01','NO02','NO04','NO06','NO07','NO08','PL01','PL02','PL06','PL08','PL09','PT01','PT02','PT04','PT05','RO02','RO03','RO04','RO05','RO06','RO07','RO08','RS01','RS02','RS03','RS04','SE01','SE02','SE03','SE04','SI01','SI02','SI03','SI04','SI05','SK01','SK02','SK03','UA02','UA04','UA05','UA06','UA07','UA08']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in europe:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 100:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/europe.png")
plt.clf()

nAmerica = ['CA01','CA02','CA03','CA04','CA05','CA06','CA07','CA08','CA09','CA10','CA11','MX01','MX02','MX03','MX04','MX05','MX06','US01','US02','US04','US05','US06','US07','US09','US12','US14','US15','US16','US17','US19','US20','US23']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in nAmerica:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 100:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/nAmerica.png")
plt.clf()

sAmerica = ['AR01','AR02','AR03','AR04','AR05','BR01','BR02','BR03','BR05','BR06','BR12','BR13','CL01','CL02','CL03','CL05','CL06','CO01','CO02','CO03','CO04','PE01','PE02','PE03','PE04']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in sAmerica:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 200:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/sAmerica.png")
plt.clf()

africa = ['EG01','EG02','EG03','IL01','IL02','IL03','IL04','MA01','MA02','SA02','SA03','SA04','ZA01','ZA02','ZA03','ZA04','ZA05','ZA06','ZA07']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in africa:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 0:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/africa.png")
plt.clf()

asiaOceania = ['AU02','AU05','AU06','AU07','AU08','CN02','CN03','CN04','CN05','ID01','ID02','ID03','ID04','ID05','IN01','IN02','IN03','IN04','IN06','IN07','IN08','IN09','JP02','JP03','JP04','JP05','JP06','JP07','JP09','KR02','KR06','KR07','KZ01','KZ02','MY01','MY02','MY03','MY04','NZ01','NZ03','NZ05','NZ06','PH01','PH04','PH05','PH06','PH07','PK01','PK02','PK03','PK04','PK05','PK06','RU02','RU05','RU11','RU20','RU21','RU22','RU23','TH01','TH02','TH03','TH04','TR01','TR02','TR03','TR04','TR05','TR06','TW01','TW02','TW03','TW05','VN01','VN02','VN03','VN04','VN05','VN06']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

for ispOp in asiaOceania:
    ispData = data2[data2.isp == ispOp].reset_index(drop=True)
    if len(ispData) > 800:
        plt.plot(ispData['Date_First_Seen'], range(0,len(ispData)), label=ispOp)

plt.xlabel("time (mm/yy)")
plt.ylabel("total amount of new infections observed")
plt.legend(bbox_to_anchor=(0.25, 1))
plt.savefig("images/block3/asia_oceania.png")
plt.clf()







