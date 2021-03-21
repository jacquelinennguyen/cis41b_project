# Name: Fawaz Al-Harbi
# Implementation file for the web scraping part of the backend of the TopCharts program

import requests
from bs4 import BeautifulSoup
import json
import time
import threading
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR

SONG_LIMIT = 100
ALBUM_LIMIT = 200
ARTIST_LIMIT = 500
STEP_AMOUNT = 100

dayToday = date.today().strftime("%d")
lastFriday = datetime.now() + relativedelta(days=-1, weekday=FR(-2) if dayToday == "Fri" else FR(-1))
monthLetter = lastFriday.strftime("%b")
monthNumber = lastFriday.strftime("%m")
day = lastFriday.strftime("%d")
year = lastFriday.strftime("%Y")

top100Songs = {}
top200Albums = {}
top500Artists = {}


# SONGS ================================================================================================================

def scrapeSongsChart():
    global top100Songs

    threadsList = []
    rvList = []

    threadsList.append(threading.Thread(target=scrapeFirstSong, args=(rvList,)))
    for startingCount in range(0, SONG_LIMIT - STEP_AMOUNT + 1, STEP_AMOUNT):
        thread = threading.Thread(target=scrapeSongBatch, args=(startingCount, rvList))
        threadsList.append(thread)
    for thread in threadsList:
        thread.start()
    for thread in threadsList:
        thread.join()

    sortedList = sorted(rvList, key=lambda x: x[0])
    for dataTuple in sortedList:
        top100Songs.update(dataTuple[1])


def scrapeFirstSong(dataContainer):
    response = requests.get(f"https://www.rollingstone.com/charts/songs/{year}-{monthNumber}-{day}/")
    soup = BeautifulSoup(response.content, "lxml")

    songName = soup.select_one("div.c-chart__table--title").text

    artist = soup.select_one("div.c-chart__table--caption").text

    unitsTrend = soup.select_one("div.c-chart__table--linegraph")["data-trend-data"]

    peakPosition = soup.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
    try:
        peakPosition = int(peakPosition)
    except ValueError:
        peakPosition = None

    weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    try:
        weeksOnChart = int(weeksOnChart)
    except ValueError:
        weeksOnChart = None

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

    try:
        coverImg = soup.select_one("img.c-chart__table--cover")["src"]
    except TypeError:
        coverImg = None

    firstData = {songName: {"artist": artist,
                            "unitsTrend": unitsTrend,
                            "peakPosition": peakPosition,
                            "weeksOnChart": weeksOnChart,
                            "label": label,
                            "topCities": topCities,
                            "songStreams": songStreams,
                            "coverImg": coverImg}}

    dataToSendBack = (-1, firstData)
    dataContainer.append(dataToSendBack)


def scrapeSongBatch(counterStart, dataContainer):
    songDataDict = {}
    response = requests.get("https://www.rollingstone.com/wp-admin/admin-ajax.php?"
                            f"counter={counterStart}"
                            "&chart=songs"
                            f"&results_per={STEP_AMOUNT}"
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
        try:
            peakPosition = int(peakPosition)
        except ValueError:
            peakPosition = None

        weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
        try:
            weeksOnChart = int(weeksOnChart)
        except ValueError:
            weeksOnChart = None

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
        try:
            songStreams = float(songStreams)
        except ValueError:
            songStreams = None

        try:
            coverImg = elem.select_one("img.c-chart__table--cover")["src"]
        except TypeError:
            coverImg = None

        songDataDict[songName] = {"artist": artist,
                                  "unitsTrend": unitsTrend,
                                  "peakPosition": peakPosition,
                                  "weeksOnChart": weeksOnChart,
                                  "label": label,
                                  "topCities": topCities,
                                  "songStreams": songStreams,
                                  "coverImg": coverImg}

    dataToSendBack = (counterStart, songDataDict)
    dataContainer.append(dataToSendBack)


# ALBUMS ===============================================================================================================

def scrapeAlbumsChart():
    global top200Albums

    threadsList = []
    rvList = []

    threadsList.append(threading.Thread(target=scrapeFirstAlbum, args=(rvList,)))
    for startingCount in range(0, ALBUM_LIMIT - STEP_AMOUNT + 1, STEP_AMOUNT):
        thread = threading.Thread(target=scrapeAlbumBatch, args=(startingCount, rvList))
        threadsList.append(thread)
    for thread in threadsList:
        thread.start()
    for thread in threadsList:
        thread.join()

    sortedList = sorted(rvList, key=lambda x: x[0])
    for dataTuple in sortedList:
        top200Albums.update(dataTuple[1])


def scrapeFirstAlbum(dataContainer):
    response = requests.get(f"https://www.rollingstone.com/charts/albums/{year}-{monthNumber}-{day}/")
    soup = BeautifulSoup(response.content, "lxml")

    albumName = soup.select_one("div.c-chart__table--title").text

    artist = soup.select_one("div.c-chart__table--caption").text

    albumUnits = soup.select_one("div.c-chart__table--stat-base.c-chart__table--album-units span").text
    albumUnits = albumUnits.replace('B', 'e9')
    albumUnits = albumUnits.replace('M', 'e6')
    albumUnits = albumUnits.replace('K', 'e3')
    try:
        albumUnits = float(albumUnits)
    except ValueError:
        albumUnits = None

    albumSales = soup.select_one("div.c-chart__table--stat-base.c-chart__table--album-sales span").text
    albumSales = albumSales.replace('B', 'e9')
    albumSales = albumSales.replace('M', 'e6')
    albumSales = albumSales.replace('K', 'e3')
    try:
        albumSales = float(albumSales)
    except ValueError:
        albumSales = None

    songSales = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-sales span").text
    songSales = songSales.replace('B', 'e9')
    songSales = songSales.replace('M', 'e6')
    songSales = songSales.replace('K', 'e3')
    try:
        songSales = float(songSales)
    except ValueError:
        songSales = None

    peakPosition = soup.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
    try:
        peakPosition = int(peakPosition)
    except ValueError:
        peakPosition = None

    weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    try:
        weeksOnChart = int(weeksOnChart)
    except ValueError:
        weeksOnChart = None

    label = soup.select_one("span.c-chart__table--label-text").text

    topSongs = []
    for liTag in soup.select("div.c-chart__table--side div.c-chart__table--cities.c-chart__table--songs li"):
        topSongs.append(liTag.text)

    songStreams = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
    songStreams = songStreams.replace('B', 'e9')
    songStreams = songStreams.replace('M', 'e6')
    songStreams = songStreams.replace('K', 'e3')
    try:
        songStreams = float(songStreams)
    except ValueError:
        songStreams = None

    try:
        coverImg = soup.select_one("img.c-chart__table--cover")["src"]
    except TypeError:
        coverImg = None

    firstData = {albumName: {"artist": artist,
                             "albumUnits": albumUnits,
                             "albumSales": albumSales,
                             "songSales": songSales,
                             "peakPosition": peakPosition,
                             "weeksOnChart": weeksOnChart,
                             "label": label,
                             "topSongs": topSongs,
                             "songStreams": songStreams,
                             "coverImg": coverImg}}

    dataToSendBack = (-1, firstData)
    dataContainer.append(dataToSendBack)


def scrapeAlbumBatch(counterStart, dataContainer):
    # for the rest of the albums ==================================================
    albumDataDict = {}
    response = requests.get("https://www.rollingstone.com/wp-admin/admin-ajax.php?"
                            f"counter={counterStart}"
                            "&chart=albums"
                            f"&results_per={STEP_AMOUNT}"
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
        try:
            albumUnits = float(albumUnits)
        except ValueError:
            albumUnits = None

        albumSales = elem.select_one("div.c-chart__table--stat-base.c-chart__table--album-sales span").text
        albumSales = albumSales.replace('B', 'e9')
        albumSales = albumSales.replace('M', 'e6')
        albumSales = albumSales.replace('K', 'e3')
        try:
            albumSales = float(albumSales)
        except ValueError:
            albumSales = None

        songSales = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-sales span").text
        songSales = songSales.replace('B', 'e9')
        songSales = songSales.replace('M', 'e6')
        songSales = songSales.replace('K', 'e3')
        try:
            songSales = float(songSales)
        except ValueError:
            songSales = None

        peakPosition = elem.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
        try:
            peakPosition = int(peakPosition)
        except ValueError:
            peakPosition = None

        weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
        try:
            weeksOnChart = int(weeksOnChart)
        except ValueError:
            weeksOnChart = None

        label = elem.select_one("span.c-chart__table--label-text").text

        topSongs = []
        for liTag in elem.select("div.c-chart__table--middle div.c-chart__table--cities.c-chart__table--songs li"):
            topSongs.append(liTag.text)

        songStreams = elem.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
        songStreams = songStreams.replace('B', 'e9')
        songStreams = songStreams.replace('M', 'e6')
        songStreams = songStreams.replace('K', 'e3')
        try:
            songStreams = float(songStreams)
        except ValueError:
            songStreams = None

        try:
            coverImg = elem.select_one("img.c-chart__table--cover")["src"]
        except TypeError:
            coverImg = None

        albumDataDict[albumName] = {"artist": artist,
                                    "albumUnits": albumUnits,
                                    "albumSales": albumSales,
                                    "songSales": songSales,
                                    "peakPosition": peakPosition,
                                    "weeksOnChart": weeksOnChart,
                                    "label": label,
                                    "topSongs": topSongs,
                                    "songStreams": songStreams,
                                    "coverImg": coverImg}

    dataToSendBack = (counterStart, albumDataDict)
    dataContainer.append(dataToSendBack)


# ARTISTS ==============================================================================================================

def scrapeArtistsChart():
    global top500Artists

    threadsList = []
    rvList = []

    threadsList.append(threading.Thread(target=scrapeFirstArtist, args=(rvList,)))
    for startingCount in range(0, ARTIST_LIMIT - STEP_AMOUNT + 1, STEP_AMOUNT):
        thread = threading.Thread(target=scrapeArtistsBatch, args=(startingCount, rvList))
        threadsList.append(thread)
    for thread in threadsList:
        thread.start()
    for thread in threadsList:
        thread.join()

    sortedList = sorted(rvList, key=lambda x: x[0])
    for dataTuple in sortedList:
        top500Artists.update(dataTuple[1])


def scrapeFirstArtist(dataContainer):
    response = requests.get(f"https://www.rollingstone.com/charts/artists/{year}-{monthNumber}-{day}/")
    soup = BeautifulSoup(response.content, "lxml")

    artistName = soup.select_one("div.c-chart__table--title").text

    songStreams = soup.select_one("div.c-chart__table--stat-base.c-chart__table--song-streams span").text
    songStreams = songStreams.replace('B', 'e9')
    songStreams = songStreams.replace('M', 'e6')
    songStreams = songStreams.replace('K', 'e3')
    try:
        songStreams = float(songStreams)
    except ValueError:
        songStreams = None

    weeksOnChart = soup.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
    try:
        weeksOnChart = int(weeksOnChart)
    except ValueError:
        weeksOnChart = None

    topSong = soup.select_one("div.c-chart__table--stat-base.c-chart__table--top-song span").text

    peakPosition = 1

    try:
        coverImg = soup.select_one("img.c-chart__table--cover")["src"]
    except TypeError:
        coverImg = None

    firstData = {artistName: {"artistName": artistName,
                              "songStreams": songStreams,
                              "weeksOnChart": weeksOnChart,
                              "topSong": topSong,
                              "peakPosition": peakPosition,
                              "coverImg": coverImg}}

    dataToSendBack = (-1, firstData)
    dataContainer.append(dataToSendBack)


def scrapeArtistsBatch(counterStart, dataContainer):
    artistDataDict = {}
    # for the rest of the artists =================================================
    response = requests.get("https://www.rollingstone.com/wp-admin/admin-ajax.php?"
                            f"counter={counterStart}"
                            "&chart=artists"
                            f"&results_per={STEP_AMOUNT}"
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
        try:
            songStreams = float(songStreams)
        except ValueError:
            songStreams = None

        weeksOnChart = elem.select_one("div.c-chart__table--stat-base.c-chart__table--weeks-present span").text
        try:
            weeksOnChart = int(weeksOnChart)
        except ValueError:
            weeksOnChart = None

        topSong = elem.select_one("div.c-chart__table--stat-base.c-chart__table--top-song span").text

        peakPosition = elem.select_one("div.c-chart__table--stat-base.c-chart__table--peak span").text
        try:
            peakPosition = int(peakPosition)
        except ValueError:
            peakPosition = None

        try:
            coverImg = elem.select_one("img.c-chart__table--cover")["src"]
        except TypeError:
            coverImg = None

        artistDataDict[artistName] = {"artistName": artistName,
                                      "songStreams": songStreams,
                                      "weeksOnChart": weeksOnChart,
                                      "topSong": topSong,
                                      "peakPosition": peakPosition,
                                      "coverImg": coverImg}

    dataToSendBack = (counterStart, artistDataDict)
    dataContainer.append(dataToSendBack)


# running the functions ================================================================================================

# threading ===================================================================
scrapingFunctions = [scrapeSongsChart, scrapeAlbumsChart, scrapeArtistsChart]
masterThreadsList = []
for function in scrapingFunctions:
    thread1 = threading.Thread(target=function)
    masterThreadsList.append(thread1)

print("starting timer")
timerStart = time.time()
for thread1 in masterThreadsList:
    thread1.start()
for thread1 in masterThreadsList:
    thread1.join()
totalTime = time.time() - timerStart
print(f"Time to fetch data: {totalTime:.2f}s")

# in sequence =================================================================
# timerStart = time.time()
#
# scrapeSongsChart()
# scrapeAlbumsChart()
# scrapeArtistsChart()
#
# totalTime = time.time() - timerStart
# print(f"Time to fetch data: {totalTime:.2f}s")
