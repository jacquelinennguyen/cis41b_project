# Jacqueline Nguyen
# getweeks will return a dictionary with all the date ranges and fridays from that date range
import pandas as pd
import datetime
from datetime import date

today = date.today()
MIN_DATE = '6/21/2019'

def allfridays(today):
    return pd.date_range(start=MIN_DATE, end=today,
        freq='W-FRI').strftime('%Y-%m-%d').tolist()

def timerange(friday) :
    fri = datetime.datetime(int(friday[:4]), int(friday[5:7]), int(friday[-2:]))
    thursday = fri + datetime.timedelta( (3-fri.weekday()) % 7 )
    fri_str = fri.strftime('%b %d, %Y')
    thur_str = thursday.strftime('%b %d, %Y')
    s = f'{fri_str} - {thur_str}'
    return s

def getweeks(today) :
    d = {}
    for friday in allfridays(today) :
        d[timerange(friday)] = friday
    return d

'''
last = allfridays(today)[-1]
print(last)
print(timerange(last))
'''
'''
for k,v in getweeks(today).items() :
    print(f'{k}: {v}')
'''