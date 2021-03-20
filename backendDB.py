# Convert to JSON and then to database.
# Should be 4 tables:
# 1: artist name key
# 2: Top 100 Songs
# 3: Top 200 Albums
# 4: Top 500 Artists

from backendWebScraper import top500Artists, top200Albums, top100Songs
import json
import sqlite3

conn = sqlite3.connect('rollingstones.db')
cur = conn.cursor()

#print(top500Artists['Taylor Swift'])

def genTableArtists(d, conn, cur) :
    cur.execute("DROP TABLE IF EXISTS ArtistsDB")      
    cur.execute('''CREATE TABLE ArtistsDB(             
                   name TEXT PRIMARY KEY,
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

'''
top200Albums[albumName] = {"artist": artist,
                               "albumUnits": albumUnits,
                               "albumSales": albumSales,
                               "songSales": songSales,
                               "peakPosition": peakPosition,
                               "weeksOnChart": weeksOnChart,
                               "label": label,
                               "topSongs": topSongs,
                               "songStreams": songStreams}
'''
def genTableAlbums(d, conn, cur) :
    cur.execute('DROP TABLE IF EXISTS AlbumsDB')
    cur.execute('''CREATE TABLE AlbumsSB(
                    artistId NOT NULL INTEGER PRIMARY KEY UNIQUE,
                    albumSales INTEGER,
                    songSales INTEGER
                    peakPosition INTEGER,
                    weeksOnChart INTEGER,
                    label TEXT,
                    topSongs TEXT,
                    songStreams INTEGER
                    )
                    ''')


#genTableArtists(top500Artists, conn, cur)