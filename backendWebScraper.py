import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3
from datetime import date
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR

dayToday = date.today().strftime("%d")
lastFriday = lastFriday = datetime.now() + relativedelta(days=-1, weekday=FR(-2) if dayToday == "Fri" else FR(-1))
# print(lastFriday)
monthLetter = lastFriday.strftime("%b")
monthNumber = lastFriday.strftime("%m")
day = lastFriday.strftime("%d")
year = lastFriday.strftime("%Y")

top100 = {}

# to get the first song of the chart ==========================================
response = requests.get(f"https://www.rollingstone.com/charts/songs/{year}-{monthNumber}-{day}/")
soup = BeautifulSoup(response.content, "lxml")

songName = soup.select_one("div.c-chart__table--title").text
# print(songName)

artist = soup.select_one("div.c-chart__table--caption").text
# print(artist)

unitsTrend = soup.select_one("div.c-chart__table--linegraph")["data-trend-data"]
# print(unitsTrend)

peakPosition = soup.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
peakPosition = int(peakPosition) if peakPosition else None
# print(peakPosition)

weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
weeksOnChart = int(weeksOnChart) if weeksOnChart else None
# print(weeksOnChart)

label = soup.select_one("span.c-chart__table--label-text").text
# print(label)

topCities = []
for liTag in soup.select("div.c-chart__table--bottom "
                         "div.c-chart__table--cities "
                         "li"):
    topCities.append(liTag.text)
# print(topCities)

songStreams = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
# print(songStreams)
rep = songStreams.replace('B', 'e9')
rep = rep.replace('M', 'e6')
rep = rep.replace('K', 'e3')
# print(float(rep))

# print()

top100[songName] = {"artist": artist,
                    "unitsTrend": unitsTrend,
                    "peakPosition": peakPosition,
                    "weeksOnChart": weeksOnChart,
                    "label": label,
                    "topCities": topCities,
                    "songStreams": rep}

# to get the rest of the songs ================================================
response = requests.get("https://www.rollingstone.com/wp-admin/admin-ajax.php?"
                        "counter=0"
                        "&chart=songs"
                        "&results_per=100"
                        f"&chart_date={monthLetter}%20{day}%2C%20{year}"
                        "&is_eoy=0"
                        "&eoy_year=0"
                        "&action=rscharts_fetch_subchart")
data = json.loads(response.content)["data"]
soup = BeautifulSoup(data, "lxml")

for count, elem in enumerate(soup.select("section.l-section__charts.c-chart__table--single"), start=1):
    songName = elem.select_one("div.c-chart__table--title").text
    # print(songName)

    artist = elem.select_one("div.c-chart__table--caption").text
    # print(artist)

    unitsTrend = elem.select_one("div.c-chart__table--linegraph")["data-trend-data"]
    # print(unitsTrend)

    peakPosition = elem.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
    peakPosition = int(peakPosition) if peakPosition else None
    # print(peakPosition)

    weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    weeksOnChart = int(weeksOnChart) if weeksOnChart else None
    # print(weeksOnChart)

    label = elem.select_one("span.c-chart__table--label-text").text
    # print(label)

    topCities = []
    for counter, liTag in enumerate(elem.select("div.c-chart__table--genre-label-cities "
                                                "div.c-chart__table--cities "
                                                "li"), start=1):
        topCities.append(liTag.text)
    # print(topCities)

    songStreams = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
    rep = songStreams.replace('B', 'e9')
    rep = rep.replace('M', 'e6')
    rep = rep.replace('K', 'e3')
    # print(float(rep))

    top100[songName] = {"artist": artist,
                        "unitsTrend": unitsTrend,
                        "peakPosition": peakPosition,
                        "weeksOnChart": weeksOnChart,
                        "label": label,
                        "topCities": topCities,
                        "songStreams": rep}

    # print()

# print(len(top100))
