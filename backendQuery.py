# Jacqueline Nguyen
# Contains all the functions with queries used to sort data in the GUI
import sqlite3

class Chart :
    def __init__(self) :
        conn = sqlite3.connect('rollingstones.db')
        self.cur = conn.cursor()
    
    def cur(self) :
        return self.cur

class Album(Chart) :
    def __init__(self) :
        super().__init__()
        self.cur = super().cur()

    def albumsDefault(self) :
        '''
        returns the album names and album artists from the Top 200 Albums (default, album units)
        (AlbumName, AlbumArtist, AlbumUnits)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.albumUnits FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId
                                ''') :
            L.append(t)
        return L

    def albumsLabelSearch(self, label) :
        '''
        If the user wants to search for the names of albums based on the chosen record label,
        this will return a list of all the albums from that record label. Input has to be a string.
        (AlbumName, AlbumArtist)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, Labels.label 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                JOIN Labels ON AlbumsDB.labelId = Labels.id
                                WHERE Names.id = AlbumsDB.artistId
                                AND Labels.id = AlbumsDB.labelId
                                AND Labels.label = (?)''', (label, )) :
            L.append(t)
        return L

    def albumsLabel(self) :
        '''
        returns the albums clumped together by their record label
        (AlbumName, AlbumArtist, RecordLabel)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, Labels.label 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                JOIN Labels ON AlbumsDB.labelId = Labels.id
                                WHERE Names.id = AlbumsDB.artistId
                                AND Labels.id = AlbumsDB.labelId
                                ORDER BY Labels.label ASC''') :
            L.append(t)
        return L

    def albumsSales(self) :
        '''
        returns the albums from the Top 200 Albums ranked by the number of album sales.
        (AlbumName, AlbumArtist, AlbumSales)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.albumSales 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId
                                ORDER BY AlbumsDB.albumSales DESC''') :
            L.append(t)
        return L

    def albumSongSales(self) :
        '''
        returns the albums from the Top 200 Albums ranked by the number of song sales.
        (AlbumName, AlbumArtist, SongSales)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.songSales 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId
                                ORDER BY AlbumsDB.songSales DESC''') :
            L.append(t)
        return L

    def albumsSongStreams(self) :
        '''
        returns the albums from the Top 200 Albums ranked by the number of song streams.
        These numbers are an estimate are are by no means the actual number at the point of collection.
        (AlbumName, AlbumArtist, SongStreams)
        '''
        L = []
        for t in self.cur.execute('''SELECT AlbumsDB.name, Names.name, AlbumsDB.songSales 
                                FROM AlbumsDB JOIN Names ON AlbumsDB.artistId = Names.id
                                WHERE Names.id = AlbumsDB.artistId
                                ORDER BY AlbumsDB.songStreams DESC''') :
            L.append(t)
        return L

class Song(Chart) :
    def __init__(self) :
        super().__init__()
        self.cur = super().cur()

    def songsDefault(self) :
        '''
        returns the names of the Top 100 Songs (default, song units)
        (SongName, ArtistName, Units)
        '''
        L = []
        for t in self.cur.execute('''SELECT SongsDB.name, Names.name, SongsDB.unitsTrend FROM SongsDB 
                                JOIN Names on SongsDB.artistId = Names.id
                                WHERE Names.id = SongsDB.artistId''') :
            trend = t[2].split(',')
            units = int(trend[-1].replace(']',''))
            tup = (t[0], t[1], units)
            L.append(tup)
        return L

    def songsWeeks(self) :
        '''
        sorts the songs by the number of weeks it's been on the chart
        (SongName, Weeks)
        '''
        L = []
        for t in self.cur.execute('''SELECT name, weeksOnChart FROM SongsDB
                                ORDER BY weeksOnChart DESC''') :
            L.append(t)
        return L

    def songsSales(self) :
        '''
        returns the songs sorted by the sale units
        '''
        return self.songsDefault()


class Artist(Chart) :
    def __init__(self) :
        super().__init__()
        self.cur = super().cur()

    def artistsDefault(self) :
        '''
        returns the names of the Top 500 Artists (default)
        (ArtistName, Streams)
        '''
        L = []
        for t in self.cur.execute('''SELECT name, songStreams FROM ArtistsDB
                                    ORDER BY songStreams DESC''') :
            L.append(t)
        return L

    def artistsWeeksChart(self) :
        '''
        returns the Artists sorted by the Number of Weeks they've been on the Chart
        (ArtistName, Weeks)
        '''
        L = []
        for t in self.cur.execute('''SELECT name, weeksOnChart FROM ArtistsDB
                                ORDER BY weeksOnChart DESC''') :
            L.append(t)
        return L

'''
s = Song()
for t in s.songsDefault() :
    print(t[2])
'''