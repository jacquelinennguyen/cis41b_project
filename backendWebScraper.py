import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3
import time
import threading
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR

dayToday = date.today().strftime("%d")
lastFriday = datetime.now() + relativedelta(days=-1, weekday=FR(-2) if dayToday == "Fri" else FR(-1))
# print(lastFriday)
monthLetter = lastFriday.strftime("%b")
monthNumber = lastFriday.strftime("%m")
day = lastFriday.strftime("%d")
year = lastFriday.strftime("%Y")

top100Songs = {}
top200Albums = {}
top500Artists = {}

timerStart = time.time()
# SONGS ===============================================================================================================

# to get the first song of the chart ==========================================
response = requests.get(f"https://www.rollingstone.com/charts/songs/{year}-{monthNumber}-{day}/")
soup = BeautifulSoup(response.content, "lxml")

songName = soup.select_one("div.c-chart__table--title").text

artist = soup.select_one("div.c-chart__table--caption").text

unitsTrend = soup.select_one("div.c-chart__table--linegraph")["data-trend-data"]

peakPosition = soup.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
peakPosition = int(peakPosition) if peakPosition else None

weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
weeksOnChart = int(weeksOnChart) if weeksOnChart else None

label = soup.select_one("span.c-chart__table--label-text").text

topCities = []
for liTag in soup.select("div.c-chart__table--bottom "
                         "div.c-chart__table--cities "
                         "li"):
    topCities.append(liTag.text)

songStreams = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
songStreams = songStreams.replace('B', 'e9')
songStreams = songStreams.replace('M', 'e6')
songStreams = songStreams.replace('K', 'e3')
songStreams = float(songStreams) if songStreams else None

# print(songName)
# print(artist)
# print(unitsTrend)
# print(peakPosition)
# print(weeksOnChart)
# print(label)
# print(topCities)
# print(songStreams)
# print()

top100Songs[songName] = {"artist": artist,
                         "unitsTrend": unitsTrend,
                         "peakPosition": peakPosition,
                         "weeksOnChart": weeksOnChart,
                         "label": label,
                         "topCities": topCities,
                         "songStreams": songStreams}

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

for elem in soup.select("section.l-section__charts.c-chart__table--single"):
    songName = elem.select_one("div.c-chart__table--title").text

    artist = elem.select_one("div.c-chart__table--caption").text

    unitsTrend = elem.select_one("div.c-chart__table--linegraph")["data-trend-data"]

    peakPosition = elem.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
    peakPosition = int(peakPosition) if peakPosition else None

    weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    weeksOnChart = int(weeksOnChart) if weeksOnChart else None

    label = elem.select_one("span.c-chart__table--label-text").text

    topCities = []
    for counter, liTag in enumerate(elem.select("div.c-chart__table--genre-label-cities "
                                                "div.c-chart__table--cities "
                                                "li"), start=1):
        topCities.append(liTag.text)

    songStreams = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
    songStreams = songStreams.replace('B', 'e9')
    songStreams = songStreams.replace('M', 'e6')
    songStreams = songStreams.replace('K', 'e3')
    songStreams = float(songStreams) if songStreams else None

    top100Songs[songName] = {"artist": artist,
                             "unitsTrend": unitsTrend,
                             "peakPosition": peakPosition,
                             "weeksOnChart": weeksOnChart,
                             "label": label,
                             "topCities": topCities,
                             "songStreams": songStreams}

    # print(songName)
    # print(artist)
    # print(unitsTrend)
    # print(peakPosition)
    # print(weeksOnChart)
    # print(label)
    # print(topCities)
    # print(songStreams)
    # print()


# ALBUMS ===============================================================================================================

# first the rank 1 album ======================================================
response = requests.get(f"https://www.rollingstone.com/charts/albums/{year}-{monthNumber}-{day}/")
soup = BeautifulSoup(response.content, "lxml")

albumName = soup.select_one("div.c-chart__table--title").text

artist = soup.select_one("div.c-chart__table--caption").text

albumUnits = soup.select_one("div.c-chart__table--stat-base.c-chart__table--album-units span").text
albumUnits = albumUnits.replace('B', 'e9')
albumUnits = albumUnits.replace('M', 'e6')
albumUnits = albumUnits.replace('K', 'e3')
albumUnits = float(albumUnits) if albumUnits else None

albumSales = soup.select_one("div.c-chart__table--stat-base.c-chart__table--album-sales span").text
albumSales = albumSales.replace('B', 'e9')
albumSales = albumSales.replace('M', 'e6')
albumSales = albumSales.replace('K', 'e3')
albumSales = float(albumSales) if albumSales else None

songSales = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-sales span").text
songSales = songSales.replace('B', 'e9')
songSales = songSales.replace('M', 'e6')
songSales = songSales.replace('K', 'e3')
songSales = float(songSales) if songSales else None

peakPosition = soup.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
peakPosition = int(peakPosition) if peakPosition else None

weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
weeksOnChart = int(weeksOnChart) if weeksOnChart else None

label = soup.select_one("span.c-chart__table--label-text").text

topSongs = []
for liTag in soup.select("div.c-chart__table--side div.c-chart__table--cities.c-chart__table--songs li"):
    topSongs.append(liTag.text)

songStreams = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
songStreams = songStreams.replace('B', 'e9')
songStreams = songStreams.replace('M', 'e6')
songStreams = songStreams.replace('K', 'e3')
songStreams = float(songStreams) if songStreams else None

# print(albumName)
# print(artist)
# print(albumUnits)
# print(albumSales)
# print(songSales)
# print(peakPosition)
# print(weeksOnChart)
# print(label)
# print(topSongs)
# print(songStreams)
# print()

top200Albums[albumName] = {"artist": artist,
                           "albumUnits": albumUnits,
                           "albumSales": albumSales,
                           "songSales": songSales,
                           "peakPosition": peakPosition,
                           "weeksOnChart": weeksOnChart,
                           "label": label,
                           "topSongs": topSongs,
                           "songStreams": songStreams}

# for the rest of the albums ==================================================
response = requests.get("https://www.rollingstone.com/wp-admin/admin-ajax.php?"
                        "counter=0"
                        "&chart=albums"
                        "&results_per=100"
                        f"&chart_date={monthLetter}%20{day}%2C%20{year}"
                        "&is_eoy=0"
                        "&eoy_year=0"
                        "&action=rscharts_fetch_subchart")
data = json.loads(response.content)["data"]
soup = BeautifulSoup(data, "lxml")

for elem in soup.select("section.l-section__charts.c-chart__table--single"):
    albumName = elem.select_one("div.c-chart__table--title").text

    artist = elem.select_one("div.c-chart__table--caption").text

    albumUnits = elem.select_one("div.c-chart__table--stat-base.c-chart__table--album-units span").text
    albumUnits = albumUnits.replace('B', 'e9')
    albumUnits = albumUnits.replace('M', 'e6')
    albumUnits = albumUnits.replace('K', 'e3')
    albumUnits = float(albumUnits) if albumUnits else None

    albumSales = elem.select_one("div.c-chart__table--stat-base.c-chart__table--album-sales span").text
    albumSales = albumSales.replace('B', 'e9')
    albumSales = albumSales.replace('M', 'e6')
    albumSales = albumSales.replace('K', 'e3')
    albumSales = float(albumSales) if albumSales else None

    songSales = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-sales span").text
    songSales = songSales.replace('B', 'e9')
    songSales = songSales.replace('M', 'e6')
    songSales = songSales.replace('K', 'e3')
    songSales = float(songSales) if songSales else None

    peakPosition = elem.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
    peakPosition = int(peakPosition) if peakPosition else None

    weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    weeksOnChart = int(weeksOnChart) if weeksOnChart else None

    label = elem.select_one("span.c-chart__table--label-text").text

    topSongs = []
    for liTag in elem.select("div.c-chart__table--middle div.c-chart__table--cities.c-chart__table--songs li"):
        topSongs.append(liTag.text)

    songStreams = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
    songStreams = songStreams.replace('B', 'e9')
    songStreams = songStreams.replace('M', 'e6')
    songStreams = songStreams.replace('K', 'e3')
    songStreams = float(songStreams) if songStreams else None

    # print(albumName)
    # print(artist)
    # print(albumUnits)
    # print(albumSales)
    # print(songSales)
    # print(peakPosition)
    # print(weeksOnChart)
    # print(label)
    # print(topSongs)
    # print(songStreams)
    # print()

    top200Albums[albumName] = {"artist": artist,
                               "albumUnits": albumUnits,
                               "albumSales": albumSales,
                               "songSales": songSales,
                               "peakPosition": peakPosition,
                               "weeksOnChart": weeksOnChart,
                               "label": label,
                               "topSongs": topSongs,
                               "songStreams": songStreams}


# ARTISTS ==============================================================================================================

# for the rank 1 artist =======================================================
response = requests.get(f"https://www.rollingstone.com/charts/artists/{year}-{monthNumber}-{day}/")
soup = BeautifulSoup(response.content, "lxml")

artistName = soup.select_one("div.c-chart__table--title").text

songStreams = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
songStreams = songStreams.replace('B', 'e9')
songStreams = songStreams.replace('M', 'e6')
songStreams = songStreams.replace('K', 'e3')
songStreams = float(songStreams) if songStreams else None

weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
weeksOnChart = int(weeksOnChart) if weeksOnChart else None

topSong = soup.select_one("div.c-chart__table--stat-base.c-chart__table--top-song span").text

peakPosition = 1

# print(artistName)
# print(songStreams)
# print(weeksOnChart)
# print(topSong)
# print(peakPosition)
# print()

top500Artists[artistName] = {"artistName": artistName,
                             "songStreams": songStreams,
                             "weeksOnChart": weeksOnChart,
                             "weeksOnChart": weeksOnChart,
                             "topSong": topSong,
                             "peakPosition": peakPosition}


# for the rest of the artists =================================================
response = requests.get("https://www.rollingstone.com/wp-admin/admin-ajax.php?"
                        "counter=0"
                        "&chart=artists"
                        "&results_per=500"
                        f"&chart_date={monthLetter}%20{day}%2C%20{year}"
                        "&is_eoy=0"
                        "&eoy_year=0"
                        "&action=rscharts_fetch_subchart")
data = json.loads(response.content)["data"]
soup = BeautifulSoup(data, "lxml")

for elem in soup.select("section.l-section__charts.c-chart__table--single"):
    artistName = elem.select_one("div.c-chart__table--title").text

    songStreams = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
    songStreams = songStreams.replace('B', 'e9')
    songStreams = songStreams.replace('M', 'e6')
    songStreams = songStreams.replace('K', 'e3')
    songStreams = float(songStreams) if songStreams else None

    weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    weeksOnChart = int(weeksOnChart) if weeksOnChart else None

    topSong = elem.select_one("div.c-chart__table--stat-base.c-chart__table--top-song span").text

    peakPosition = elem.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
    peakPosition = int(peakPosition) if peakPosition else None

    # print(artistName)
    # print(songStreams)
    # print(weeksOnChart)
    # print(topSong)
    # print(peakPosition)
    # print()

    top500Artists[artistName] = {"artistName": artistName,
                                 "songStreams": songStreams,
                                 "weeksOnChart": weeksOnChart,
                                 "weeksOnChart": weeksOnChart,
                                 "topSong": topSong,
                                 "peakPosition": peakPosition}

totalTime = time.time() - timerStart
print(f"Time to fetch data: {totalTime:.2f}s")


