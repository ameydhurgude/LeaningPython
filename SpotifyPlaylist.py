#This is a program that will make a sqlite database of your Spotify Playlists.
#To extract your laylist into a JSON file :- 
#1. Go to https://exportify.net/ and download the csv file.
#2. Convert your file into JSON using any web based converter on Google.


import sqlite3
import json

conn = sqlite3.connect('yourfilename.sqlite')
cur = conn.cursor()

fname = open('yourplaylistfile.json').read()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Popularity;


CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT 
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT 
);
CREATE TABLE Popularity (
    popularity  INTEGER NOT NULL 
         );
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  ,
    album_id  INTEGER,
    len INTEGER, 
    popularity INTEGER,
    genre TEXT
);

''')

data = fname
info = json.loads(data)
# print(info)
data_print = json.dumps(info, indent=4)
# print(data)


for i in range(len(info)):
    name = info[i]['Track Name']
    artist = info[i]['Artist Name(s)']
    album = info[i]['Album Name']
    popularity = info[i]['Popularity']
    genres = info[i]['Genres']
    length = info[i]['Duration (ms)']


    def convertTime(time):
        millis = int(time)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        return minutes


    length = convertTime(length)

    cur.execute("INSERT INTO ARTIST(name) VALUES(?)", (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
            VALUES ( ?, ? )''', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
            (title, album_id, len,popularity,genre) 
            VALUES ( ?, ?, ?, ?, ?)''',
                (name, album_id, length, popularity, genres))

conn.commit()
cur.execute("SELECT * FROM Track")
print(cur.fetchall())
