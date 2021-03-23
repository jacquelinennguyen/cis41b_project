# Jacqueline Nguyen

# Convert to database.
# Should be 4 tables:
# 1: artist name key
# 2: Top 100 Songs
# 3: Top 200 Albums
# 4: Top 500 Artists
import importlib
import backendWebScraper
importlib.reload(backendWebScraper)
from backendWebScraper import top500Artists, top200Albums, top100Songs
import json
import sqlite3
import re
import threading

lock = threading.Lock()

def genTableArtists(d, conn, cur) :
    '''
    Generate table for Top 500 Artists.
    '''
    cur.execute("DROP TABLE IF EXISTS ArtistsDB")      
    cur.execute('''CREATE TABLE ArtistsDB(             
                   name TEXT NOT NULL UNIQUE,
                   songStreams INTEGER,
                   weeksOnChart INTEGER,
                   topSong TEXT,
                   peakPosition INTEGER,
                   coverImg TEXT)''')

    for k, v in d.items() :
        cur.execute('''INSERT INTO ArtistsDB 
                        (name, songStreams, weeksOnChart, topSong, peakPosition, coverImg) 
                        VALUES (?, ?, ?, ?, ?, ?)''',
                        (k, v['songStreams'], v['weeksOnChart'], v['topSong'], v['peakPosition'], v["coverImg"]))
    conn.commit()

def genTableAlbumsSongs(d1, d2, conn, cur) :
    '''
    Generate :
    1)  Top 200 Albums Table
    2)  Top 100 Songs Table
    3)  Artist Name Key Table
    '''

    cur.execute('DROP TABLE IF EXISTS Names')
    cur.execute('''CREATE TABLE Names(
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT UNIQUE ON CONFLICT IGNORE
    )
    ''')

    cur.execute('DROP TABLE IF EXISTS Labels')
    cur.execute('''CREATE TABLE Labels(
            id INTEGER NOT NULL PRIMARY KEY,
            label TEXT UNIQUE ON CONFLICT IGNORE
        )
        ''')

    cur.execute('DROP TABLE IF EXISTS AlbumsDB')
    cur.execute('''CREATE TABLE AlbumsDB(
                    name TEXT NOT NULL,
                    artistId INTEGER,
                    albumUnits INTEGER,
                    albumSales INTEGER,
                    songSales INTEGER,
                    peakPosition INTEGER,
                    weeksOnChart INTEGER,
                    topSongs TEXT,
                    labelId INTEGER,
                    songStreams INTEGER,
                    coverImg TEXT
                    )
                    ''')

    cur.execute('DROP TABLE IF EXISTS SongsDB')
    cur.execute('''CREATE TABLE SongsDB(
            name TEXT NOT NULL,
            artistId INTEGER,
            unitsTrend INTEGER,
            peakPosition INTEGER,
            labelId INTEGER,
            topCities TEXT,
            weeksOnChart INTEGER,
            streams INTEGER,
            coverImg TEXT
            )''')



    for k, v in d2.items() :
        artist = v['artist']
        artist = re.sub(r'feat\..*', '', artist).rstrip()
        cur.execute('''INSERT INTO Names (name) VALUES (?)''', (artist,))
        cur.execute('''SELECT id FROM Names WHERE name = ?''', (artist,))
        artist_id = cur.fetchone()[0]
        label = v['label']
        cur.execute('''INSERT INTO Labels (label) VALUES (?)''', (label,))
        cur.execute('''SELECT id FROM Labels WHERE label = ?''', (label,))
        label_id = cur.fetchone()[0]
        #print(k)
        topSongs = v['topSongs']
        topSongs = ", ".join(topSongs)
        # print(k)
        cur.execute('''INSERT INTO AlbumsDB
                (name, artistId, albumUnits, albumSales, songSales, 
                peakPosition, weeksOnChart, labelId, topSongs, songStreams, coverImg) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (k, artist_id, v['albumUnits'], v['albumSales'], v['songSales'],
                      v['peakPosition'], v['weeksOnChart'], label_id, topSongs, v['songStreams'], v["coverImg"]))
    conn.commit()
    for k, v in d1.items() :
        artist = v['artist']
        artist = re.sub(r'feat\..*', '', artist).rstrip()
        #print(artist)
        cur.execute('''INSERT INTO Names (name) VALUES (?)''', (artist,))
        cur.execute('''SELECT id FROM Names WHERE name = ?''', (artist,))
        artist_id = cur.fetchone()[0]
        label = v['label']
        cur.execute('''INSERT INTO Labels (label) VALUES (?)''', (label,))
        cur.execute('''SELECT id FROM Labels WHERE label = ?''', (label,))
        label_id = cur.fetchone()[0]
        
        cities = ""
        for i in range(len(v['topCities'])) :
            city = v['topCities'][i]
            s = f'{i+1} {city}\n'
            cities += s

        cur.execute('''INSERT INTO SongsDB
                (name, artistId, unitsTrend, peakPosition, labelId, topCities, weeksOnChart, streams, coverImg) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (k, artist_id, v['unitsTrend'], v['peakPosition'], label_id,
                      cities, v['weeksOnChart'], v['songStreams'], v["coverImg"]))
    
    conn.commit()

def updateDB() :
    #lock.acquire()
    conn = sqlite3.connect('rollingstones.db')
    cur = conn.cursor()
    #print(list(top100Songs.keys())[:10])
    genTableArtists(top500Artists, conn, cur)
    genTableAlbumsSongs(top100Songs, top200Albums, conn, cur)
    conn.close()
    #lock.release()

# updateDB()
#print(top100Songs['drivers license'])
#print(top200Albums['Kid Krow'])