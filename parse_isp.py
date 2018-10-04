import pandas as pd
import sys

data = pd.read_csv('data_miraibadpackets.csv', sep=';', na_filter = False)
asn_types = pd.read_csv('asn_types.csv', na_filter=False)
op_names = pd.read_csv('op_names.csv', na_filter=False)

# for each ASN in the database, find the corresponding ISP
ops = list()
asnseries = asn_types['asn']
c = 0
for asn in data['ASN']:
    # find the position of the ASN in the asn_types list, strip the letters AS
    # some entries don't have an ASN
    if asn == "ASNA":
        i = list()
    else:
        i = asnseries[asnseries == int(asn[2:])]
    if len(i) == 0 :
        op = "NULL"
    else:
        op = asn_types['tg_op'][i.index[0]]
    ops.append(op)
    c = c + 1
    if c % 1000 == 0:
        print "{0:.1f}%".format(c/float(len(data))*100)
        sys.stdout.write("\033[F")

print "100.0%"

data['isp'] = ops

data.to_csv('data_maraibadpackets_isp.csv', sep=';', index=False, encoding='utf-8')

