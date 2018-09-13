import sys
import pandas as pd
from datetime import datetime
import dateutil.parser as parser
import requests as rq
import thread
import time

site = "http://mirai.badpackets.net"
total_pages = 0
total_records = 0
session = rq.session()
columns = ["IP_Address","Autonomous_System", "Country", "ASN", "Date_First_Seen"]

# Fetches all the entries on the requested page p
# The entries on the page or stored in a dataframe which is stored for later usage
def fetchPage(p):
    pageDf = pd.DataFrame(columns=columns)
    page = session.get(site + "/?page=" + str(p))
    content = page.text
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
            pageDf = pageDf.append(pd.DataFrame([[ip,asys,country,asn,dfs]], columns=columns), ignore_index=True)
        except:
            print "Exception: skipped on page {} record: {}".format(p,record)
    data[p-1] = pageDf
    print "page {} fetched".format(p)

# checks if all threads have finished, thus all records are found
def checkFinish():
    shouldWait = True
    count = 0
    while(shouldWait):
        shouldWait = False
        c = 1
        for i in data:
            # on the consecutive tries, don't spawn more than 250 threads
            if count == 50:
                time.sleep(20)
                count = 0
            if i is None or i.empty:
                thread.start_new_thread(fetchPage, (c,))
                shouldWait = True
                count = count + 1
            c = c + 1
    finish()

# concatenates all results and saves it to csv
# note that this becomes very slow for large dataframes and could be improved
def finish():
    df = pd.DataFrame(columns=columns)
    for p in range(0,total_pages):
        df = df.append(data[p],ignore_index=True)
        if p%10 == 0:
            print "concatenating data... currently page {}".format(p)
    df.to_csv("data_miraibadpackets.csv", sep=';', index=False, encoding='utf-8')
    print "Total records on website: {}\nTotal records extracted: {}".format(total_records,df[columns[0]].count())

# make an http request for the specified web page
# NOTE: the code kind of sucks, since it requests the same resources many times
# something is wrong with the storage of the results that requires it to do that
# This basically means that there is a lot of strain on the website (sorry), so
# don't try to run it if you don't have to
main():
    try:
        page = session.get(site)
        content = page.text

        # extract total number of pages
        total_pages = int(content.split("Page 1 of ")[1].split("</small>")[0])
        
        # extract total number of records, so we can verify we have all of them
        total_records = int(content.split("Total Records: ")[1].split("</span>")[0])
        
    except:
        print "exception {}".format(page)

    print "Total pages: {}".format(total_pages)

    global data = [None] * total_pages

    for page in range(1,total_pages+1):
        # spawn a thread to retrieve a page, 100 a time seems to work      
        thread.start_new_thread(fetchPage, (page,))
        if page%100 == 0:
            print "spawned threads till page {}".format(page)
            time.sleep(30)
    checkFinish()
