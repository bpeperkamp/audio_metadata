# About this application

I've written this small python aplication to get metadata from audio files. It searches through a folder for audio files and creates a database for the metadata and audio details. It is purely meant for use on the terminal/cli. Currently, it recognizes mp3, mp4, flac and wav files. Soon i'll add more file types! (dsd, ogg, etc.) It's part of a larger application i'm making, but i thought this could be of use to other people as well.

The resulting database is Sqlite file which you can use to search and query. It creates entries for the files themselves, but also artist information, album, bitrate etc.

## You can use it as following

```bash
python main.py -d /directory/music -f outfile
```

-d, or --directory is the directory to index.  
-f, or --database is the intended output file. It is optional, the default is music. (it will output music.db3 in the current path).  

The resulting database will have the "files", "metadata" and "details" tables.

### The stored information is as following

**files:**  
filename - directory - full location - file extension - index date

**metadata:**  
artist - album - song title - year/date - genre - track number - total tracks (in case of album) - file id (foreign key to files)

**details:**  
length - bits/bitrate - channels - sample rate - file id (foreign key to files)

#### A simple query would give you back your results

```sqlite3
select f.location, m.artist, m.album, m.title, m.year, m.tracknumber, m.totaltracks, d.length, d.bits, d.sample_rate from files f 
left join metadata m on f.id = m.file_id 
left join details d on f.id = d.file_id
where f.location like "%Crazy English Summer%";
```

On my old computer it indexes 1500 files within 1 minute, so it should be fast!

![Command output](/../main/screenshots/output.png?raw=true")
