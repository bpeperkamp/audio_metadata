import sqlite3
import datetime

def migrate(db_file: str):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    
    sql_statements = [ 
        """CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY, 
                name text NOT NULL, 
                location text NOT NULL, 
                directory text NOT NULL,
                extension text NOT NULL,
                index_date TIMESTAMP NOT NULL
            );""",

        """CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY, 
                artist TEXT NOT NULL,
                album TEXT,
                title TEXT,
                year TEXT,
                genre TEXT,
                tracknumber INTEGER,
                totaltracks INTEGER,
                file_id INTEGER,
                FOREIGN KEY (file_id) REFERENCES files (id)
            );""",

        """CREATE TABLE IF NOT EXISTS details (
                id INTEGER PRIMARY KEY, 
                length REAL,
                bits INTEGER,
                channels INTEGER,
                sample_rate INTEGER,
                file_id INTEGER,
                FOREIGN KEY (file_id) REFERENCES files (id)
            );"""
    ]

    for statement in sql_statements:
        cursor.execute(statement)
        connection.commit()
    
def store_file(db_file: str, file):
    connection = sqlite3.connect(db_file)
    
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=NORMAL")
    connection.execute("PRAGMA cache_size=-64000")
    connection.execute("PRAGMA mmap_size=268435456")

    sql = """INSERT INTO files(name,location,directory,extension,index_date)
              VALUES(?,?,?,?,?)"""
    
    cursor = connection.cursor()
    cursor.execute(sql, (file["name"], file["location"], file["directory"], file["extension"], datetime.datetime.now()))
    
    connection.commit()

    return cursor.lastrowid

def store_metadata(db_file: str, file_id: int, metadata):
    connection = sqlite3.connect(db_file)
    
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=NORMAL")
    connection.execute("PRAGMA cache_size=-64000")
    connection.execute("PRAGMA mmap_size=268435456")

    sql = """INSERT INTO metadata(artist,album,title,year,genre,tracknumber,totaltracks,file_id)
              VALUES(?,?,?,?,?,?,?,?)"""
    
    sql_details = """INSERT INTO details(length,bits,channels,sample_rate,file_id)
              VALUES(?,?,?,?,?)"""
    
    tracknumber = metadata.tracknumber if metadata.tracknumber is not None else 0
    totaltracks = metadata.totaltracks if metadata.totaltracks is not None else 0
    
    cursor = connection.cursor()
    cursor.execute(sql, (metadata.artist, metadata.album, metadata.title, metadata.date, metadata.genre, tracknumber, totaltracks, file_id))
    cursor.execute(sql_details, (metadata.info["length"], metadata.info["bits"], metadata.info["channels"], metadata.info["sample_rate"], file_id))

    connection.commit()