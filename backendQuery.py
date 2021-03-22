# Jacqueline Nguyen
# Contains all the functions with queries used to sort data in the GUI
# (Edited by Kaede Hamada)
import sqlite3

class Chart :
    def __init__(self) :
        self.conn = sqlite3.connect('rollingstones.db')
        self.cur = self.conn.cursor()
    
    def cur(self) :
        return self.cur

    def conn(self):
        return self.conn


class Album(Chart) :
    def __init__(self) :
        super().__init__()
        self.conn = super().conn()
        self.cur = super().cur()

    def albumsDefault(self) :
        '''
        returns the album names and album artists from the Top 200 Albums (default, album units)
        (AlbumName, AlbumArtist, AlbumUnits)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.albumUnits 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                AND Names.id = AlbumsDB.artistId''') :
            L.append(t)
        return L

    def labelsInAlbums(self) :
        '''
        returns all the record labels in the album chart
        '''
        self.cur.execute("SELECT label FROM AlbumsDB")
        return sorted(set(data[0] for data in self.cur.fetchall() if data[0] != ""))

    def topAlbumOfLabel(self, label) :
        '''
        return the chosen record label, the top album from the label, its artist and album units.
        Input has to be a string. (RecordLabel, AlbumName, AlbumArtist, AlbumUnits)
        '''
        self.cur.execute('''SELECT AlbumsDB.label, AlbumsDB.name, Names.name, AlbumsDB.albumUnits
                        FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                        AND Names.id = AlbumsDB.artistId WHERE AlbumsDB.label = ?
                        ORDER BY AlbumsDB.albumUnits DESC''', (label, ))
        return self.cur.fetchone()

    def albumsSales(self) :
        '''
        returns the albums from the Top 200 Albums ranked by the number of album sales.
        It excludes the albums with null album sales (AlbumName, AlbumArtist, AlbumSales)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.albumSales 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId 
                                AND AlbumsDB.albumSales IS NOT NULL
                                ORDER BY AlbumsDB.albumSales DESC''') :
            L.append(t)
        return L

    def albumSongSales(self) :
        '''
        returns the albums from the Top 200 Albums ranked by the number of song sales.
        It excludes the albums with null song sales(AlbumName, AlbumArtist, SongSales)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.songSales 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId
                                AND AlbumsDB.songSales IS NOT NULL
                                ORDER BY AlbumsDB.songSales DESC''') :
            L.append(t)
        return L

    def albumsSongStreams(self) :
        '''
        returns the albums from the Top 200 Albums ranked by the number of song streams.
        These numbers are an estimate are are by no means the actual number at the point of collection.
        It excludes the albums with null song streams (AlbumName, AlbumArtist, SongStreams)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.songSales 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId
                                AND AlbumsDB.songStreams IS NOT NULL
                                ORDER BY AlbumsDB.songStreams DESC''') :
            L.append(t)
        return L

    def close_conn(self):
        '''
        closes the connection to the database from an Album object
        '''
        self.conn.close()


class Song(Chart) :
    def __init__(self) :
        super().__init__()
        self.conn = super().conn()
        self.cur = super().cur()

    def songsDefault(self) :
        '''
        returns the names of the Top 100 Songs (default, song units)
        (SongName, ArtistName, Units)
        '''
        L = []
        for t in self.cur.execute('''SELECT SongsDB.name, Names.name, SongsDB.unitsTrend
                                FROM SongsDB JOIN Names ON SongsDB.artistId = Names.id
                                AND Names.id = SongsDB.artistId''') :
            L.append((t[0], t[1], int(t[2].split(',')[-1].replace(']',''))))
        return L

    def allArtistsInSongs(self):
        '''
        returns all the artist names in the song chart
        '''
        self.cur.execute('''SELECT Names.name FROM SongsDB JOIN Names
                        ON SongsDB.artistId = Names.id''')
        S = set(name[0] for name in self.cur.fetchall())
        return sorted(S, key=lambda name: name.lower())

    def maxWeeksOfArtist(self, artist) :
        '''
        returns the largest number of weeks on chart of the chosen artist
        '''
        self.cur.execute('''SELECT SongsDB.weeksOnChart FROM SongsDB JOIN Names
                        ON SongsDB.artistId = Names.id
                        AND Names.name == ? ORDER BY weeksOnChart DESC''', (artist,))
        return self.cur.fetchone()[0]

    def allSongs(self):
        '''
        returns all the songs in the song chart
        '''
        self.cur.execute("SELECT name FROM SongsDB")
        L = [name[0] for name in self.cur.fetchall()]
        return sorted(L, key=lambda name: name.lower())

    def unitsOfSong(self, song) :
        '''
        returns the song sales of the chosen song
        '''
        self.cur.execute("SELECT unitsTrend FROM SongsDB WHERE name = ?", (song,))
        return int(self.cur.fetchone()[0].split(',')[-1].replace(']',''))

    def close_conn(self):
        '''
        closes the connection to the database from a Song object
        '''
        self.conn.close()


class Artist(Chart) :
    def __init__(self) :
        super().__init__()
        self.conn = super().conn()
        self.cur = super().cur()

    def artistsDefault(self) :
        '''
        returns the names of the Top 500 Artists (default) (ArtistName, Streams)
        '''
        L = []
        for t in self.cur.execute('''SELECT name, songStreams FROM ArtistsDB
                                    ORDER BY songStreams DESC''') :
            L.append(t)
        return L

    def allArtists(self):
        '''
        return all the artist names in the artist chart
        '''
        self.cur.execute("SELECT name FROM ArtistsDB")
        L = [name[0] for name in self.cur.fetchall()]
        return sorted(L, key=lambda name: name.lower())

    def weeksOfArtist(self, artist) :
        '''
        returns the largest number of weeks on chart of the chosen artis
        '''
        self.cur.execute('''SELECT weeksOnChart FROM ArtistsDB WHERE name = ?''', (artist,))
        return self.cur.fetchone()[0]

    def songStreamsOfArtist(self, artist):
        '''
        returns the song streams of the chosen artist
        '''
        self.cur.execute('''SELECT songStreams FROM ArtistsDB WHERE name = ?''', (artist,))
        return self.cur.fetchone()[0]

    def close_conn(self):
        '''
        closes the connection to the database from an Artist object
        '''
        self.conn.close()

'''
s = Song()
for t in s.songsDefault() :
    print(t[2])
'''