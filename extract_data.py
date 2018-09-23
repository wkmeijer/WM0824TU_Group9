import urllib2,cookielib
import sys
import pandas as pd
from datetime import datetime
import dateutil.parser as parser

site = "http://mirai.badpackets.net"
total_pages = ""
total_records = ""

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

# make an http request for the specified web page
try:
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    content = page.read()

    # extract total number of pages
    total_pages = int(content.split("Page 1 of ")[1].split("</small>")[0])
    
    # extract total number of records, so we can verify we have all of them
    total_records = int(content.split("Total Records: ")[1].split("</span>")[0])
    
except:
    print "exception: {}".format(req)

print "Total pages: {}".format(total_pages)

# Create a new dataframe to store the dataset
columns = ["IP_Address","Autonomous_System", "Country", "ASN", "Date_First_Seen"]
df = pd.DataFrame(columns=columns)
count = 0
page = 1

for page in range(page,total_pages):
    req = urllib2.Request(site + "/?page=" + str(page), headers=hdr)
    page = urllib2.urlopen(req)
    content = page.read()
    records = content.split("</tbody>")[0].split("tr class")[1:]
    for record in records:
        try:
            ip = record.split("\'>")[1].split("</a")[0]
            asys = record.split("autonomousSystem\">")[1].split("</td>")[0]
            country = record.split("country\">")[1].split("</td>")[0]
            asn = record.split("asn\"><a target")[1].split("\'>")[1].split("</a>")[0]
            # strip off timezone, because parsing that is ambiguous anyway, because of summer/winter time
            dfs = record.split("firstSeen\">")[1].split(" PST</td>")[0]
            dfs = datetime.strptime(dfs, '%Y-%m-%d %H:%M:%S')
            # append record to dataset
            df = df.append(pd.DataFrame([[ip,asys,country,asn,dfs]], columns=columns), ignore_index=True)
        except:
            print "Exception: skipped on page {} record: {}".format(page,record)
    count = count + 1
    # Display progress
    if count % 10 == 0:
        print "{0:.1f}%".format(count/float(total_pages)*100)
        sys.stdout.write("\033[F")

# export total datset to CSV
df.to_csv("miraibadpackets.csv", index=False)

print "Total records on website: {}\nTotal records extracted: {}".format(total_records,df[columns[0]].count())


