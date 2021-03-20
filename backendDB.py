# Jacqueline Nguyen

# Convert to database.
# Should be 4 tables:
# 1: artist name key
# 2: Top 100 Songs
# 3: Top 200 Albums
# 4: Top 500 Artists

from backendWebScraper import top500Artists, top200Albums, top100Songs
import json
import sqlite3
import re

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
                   peakPosition INTEGER)''')

    for k, v in d.items() :
        cur.execute('''INSERT INTO ArtistsDB 
                        (name, songStreams, weeksOnChart, topSong, peakPosition) 
                        VALUES (?, ?, ?, ?, ?)''', 
                        (k, v['songStreams'], v['weeksOnChart'], v['topSong'], v['peakPosition']))
    conn.commit()

def genTableAlbumsSongs(d1, d2, conn, cur) :
    '''
    Generate :
    1)  Top 200 Albums Table
    2)  Top 100 Songs Table
    3)  Artist Name Key Table
    '''
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
                    label TEXT,
                    songStreams INTEGER
                    )
                    ''')

    cur.execute('DROP TABLE IF EXISTS SongsDB')
    cur.execute('''CREATE TABLE SongsDB(
            name TEXT NOT NULL,
            artistId INTEGER,
            unitsTrend INTEGER,
            peakPosition INTEGER,
            label TEXT,
            topCities TEXT,
            weeksOnChart INTEGER,
            streams INTEGER
            )''')

    cur.execute('DROP TABLE IF EXISTS Names')
    cur.execute('''CREATE TABLE Names(
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT UNIQUE ON CONFLICT IGNORE
    )
    ''')

    for k, v in d2.items() :
        artist = v['artist']
        artist = re.sub(r'feat\..*', '', artist).rstrip()
        cur.execute('''INSERT INTO Names (name) VALUES (?)''', (artist,))
        cur.execute('''SELECT id FROM Names WHERE name = ?''', (artist,))
        artist_id = cur.fetchone()[0]
        #print(k)
        topSongs = v['topSongs']
        topSongs = ", ".join(topSongs)
        #print(topSongs)
        cur.execute('''INSERT INTO AlbumsDB
                (name, artistId, albumUnits, albumSales, songSales, peakPosition, weeksOnChart, label, topSongs, songStreams) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (k, artist_id, v['albumUnits'], v['albumSales'], v['songSales'], v['peakPosition'], v['weeksOnChart'], v['label'], topSongs, v['songStreams']))
    conn.commit()
    for k, v in d1.items() :
        artist = v['artist']
        artist = re.sub(r'feat\..*', '', artist).rstrip()
        #print(artist)
        cur.execute('''INSERT INTO Names (name) VALUES (?)''', (artist,))
        cur.execute('''SELECT id FROM Names WHERE name = ?''', (artist,))
        artist_id = cur.fetchone()[0]
        
        cities = ""
        for i in range(len(v['topCities'])) :
            city = v['topCities'][i]
            s = f'{i+1} {city}\n'
            cities += s

        cur.execute('''INSERT INTO SongsDB
                (name, artistId, unitsTrend, peakPosition, label, topCities, weeksOnChart, streams) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (k, artist_id, v['unitsTrend'], v['peakPosition'], v['label'], cities, v['weeksOnChart'], v['songStreams']))
    
    conn.commit()

def updateDB() :
    conn = sqlite3.connect('rollingstones.db')
    cur = conn.cursor()
    genTableArtists(top500Artists, conn, cur)
    genTableAlbumsSongs(top100Songs, top200Albums, conn, cur)

updateDB()
#print(top100Songs['drivers license'])
#print(top200Albums['Future Nostalgia'])