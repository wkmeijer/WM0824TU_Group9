import pandas as pd
import pyasn
import sys

# NOTE: run with python3, python2 gives errors on the get_as_size function

asn_types = pd.read_csv('asn_types.csv', na_filter=False)
op_names = pd.read_csv('op_names.csv', na_filter=False)

# Lookup AS size, we simply pick the latest known values, as the last entry in 
# our dataset is not that long ago (2018-09-12)
# Run: 
#   pyasn_util_download.py --latest
#   pyasn_util_convert.py --single rib.yyyymmdd.1200.bz2 ipasn_yyyymmdd.dat

asndb = pyasn.pyasn('/usr/local/bin/ipasn_20181011.dat')

asnSizes = list()
print("Searching for AS sizes")
c = 0
for asn in asn_types['asn']: 
    try:
        asnSizes.append(asndb.get_as_size(asn))
    except Exception:
        asnSizes.append(0)
    c = c + 1
    if c % 10 == 0:
        print("{0:.1f}%".format(c/float(len(asn_types))*100))
        sys.stdout.write("\033[F")

print("100.0%")

# Add column of AS sizes
asn_types['size'] = asnSizes

# Aggregate AS's on ISP and add ISP size column
ispSizes = list()
print("Aggregating AS sizes to create ISP sizes")
c = 0
for isp in op_names['op']:
    ispSizes.append(asn_types[asn_types.tg_op == isp]['size'].sum())
    c = c + 1
    if c % 10 == 0:
        print("{0:.1f}%".format(c/float(len(op_names))*100))
        sys.stdout.write("\033[F")

print("100.0%")

op_names['size'] = ispSizes

asn_types.to_csv('asn_types_v2.csv', index=False, encoding='utf-8')
op_names.to_csv('op_names_v2.csv', index=False, encoding='utf-8')

