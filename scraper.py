#!/usr/bin/env python3
#
# function to scrape direction and timespan
#
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import sys

airport_code = sys.argv[1]
output_csvfile = sys.argv[2]

print("getting flight schedule for IATA code ",airport_code,", CSV output in ",output_csvfile)

#
# airport - IATA 3 letter airport code
# direction - 0 = arrivals, 1 = departures
# timespan - index of 3 hour blocks: 1 = 00:00-03:00, 2=03:00-06:00 ... , 8=21:00-00:00
#
def getFlights(airport,direction,timespan):
    urlbase = "https://www.flightstats.com/go/weblet"
    urlparams = {
        # I think this is the embedded API key that capetown-airport.co.za uses for flightstats???
        "guid":"49e3481552e7c4c9:-5b147615:12ec353094a:-205f",
        "weblet":"status",
        "action":"AirportFlightStatus",
        "airportCode":airport,
        "airportQueryType":direction,
        "airportQueryTimePeriod":timespan
    }
    
    print("send query...",airport,direction,timespan)
    rsp = requests.get(urlbase,params=urlparams)
    print("url was...",rsp.request.url)
    return rsp

def parseFlightRsp(rsp,dlabel=0):
    soup = BeautifulSoup(rsp.text, "html.parser")
    tables = soup.findAll("table")
    num_tables = len(tables)
    # this is the flight data result...found by inspection
    table = tables[4]

    all_rows = []
    rows = table.findAll("tr")
    for r in rows:
        newrow = [dlabel]
        cols = r.findAll("td")
        for c in cols:
            #
            # fix the text in the string
            cellval = c.get_text().strip()
            cellval = cellval.replace("\n","$")
            newrow.append(cellval)
        all_rows.append(newrow)
    return all_rows


all_rows = []
directions = {0:"Dep",1:"Arr"}
timeblocks = [1,2,3,4,5,6,7,8]

for t in timeblocks:
    for d,dl in directions.items():
        print(d,dl)
        rsp = getFlights(airport_code,d,t)
        rows = parseFlightRsp(rsp,dlabel=dl)
        all_rows = all_rows + rows
        print("found",len(rows),"records")
        
with open(output_csvfile,"w") as f:
    csvout = csv.writer(f)
    csvout.writerows(all_rows)

