# Jacqueline Nguyen
# getweeks will return a dictionary with all the date ranges and fridays from that date range
import pandas as pd
import datetime
from datetime import date
import requests
from bs4 import BeautifulSoup

response = requests.get(f"https://www.rollingstone.com/charts/songs/")
soup = BeautifulSoup(response.content, "lxml")

for tag in soup.select("input#rs-charts-datepicker") :
    MIN_DATE = tag['data-min-date']
    MAX_DATE = tag['data-max-date']

def allfridays(max_date):
    return pd.date_range(start=MIN_DATE, end=max_date,
        freq='W-FRI').strftime('%Y-%m-%d').tolist()

def timerange(friday) :
    fri = datetime.datetime(int(friday[:4]), int(friday[5:7]), int(friday[-2:]))
    thursday = fri + datetime.timedelta( (3-fri.weekday()) % 7 )
    fri_str = fri.strftime('%b %d, %Y')
    thur_str = thursday.strftime('%b %d, %Y')
    s = f'{fri_str} - {thur_str}'
    return s

def getweeks(max_date) :
    d = {}
    for friday in allfridays(max_date) :
        d[timerange(friday)] = friday
    return d

'''
last = allfridays(MAX_DATE)[-1]
print(last)
print(timerange(last))
'''
'''
for k,v in getweeks(MAX_DATE).items() :
    print(f'{k}: {v}')
'''