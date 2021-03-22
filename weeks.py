# Jacqueline Nguyen
import pandas as pd
import datetime
from datetime import date

today = date.today()

def allfridays(today):
    return pd.date_range(start='6/21/2018', end=today,
        freq='W-FRI').strftime('%Y-%m-%d').tolist()

def timerange(friday) :
    fri = datetime.datetime(int(friday[:4]), int(friday[5:7]), int(friday[-2:]))
    thursday = fri + datetime.timedelta( (3-today.weekday()) % 7 )
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
print(timerange(last))
#print(formatDate(today))
'''

print(getweeks(today))