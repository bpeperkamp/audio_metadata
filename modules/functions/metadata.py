from dataclasses import dataclass
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3

@dataclass()
class MetaData:
    artist: str
    album: str
    title: str
    date: str
    tracknumber: int
    totaltracks: int
    label: str
    genre: str
    comment: str
    info: dict

def create_from(file: dict) -> MetaData:
    if file['extension'] == 'flac':
        data = FLAC(file['location'])

        info = {
            "length": data.info.length,
            "bits": data.info.bits_per_sample,
            "channels": data.info.channels,
            "sample_rate": data.info.sample_rate
        }

        # track and tracktotal can be a combined string eg: 4/20
        if '/' in data['tracknumber'][0]:
            trackdata = data['tracknumber'][0].split('/', 1)
            tracknumber = trackdata[0]
            tracktotal = trackdata[1]
        else:
            tracknumber = data['tracknumber'][0] if 'tracknumber' in data else 0
            tracktotal = data['totaltracks'][0] if 'totaltracks' in data else data['tracktotal'][0] if 'tracktotal' in data else 0
            
        metadata = MetaData(
            artist = data['artist'][0] if 'artist' in data else str(None),
            album = data['album'][0] if 'album' in data else str(None),
            title = data['title'][0] if 'title' in data else str(None),
            date = data['date'][0] if 'date' in data else str(None),
            tracknumber = tracknumber,
            totaltracks = tracktotal,
            label = data['label'][0] if 'label' in data else str(None),
            genre = data['genre'][0] if 'genre' in data else str(None),
            comment = data['comment'][0] if 'comment' in data else str(None),
            info = info
        )

        return metadata
    
    if file['extension'] == 'wav':
        data = WAVE(file['location'])

        info = {
            "length": data.info.length,
            "bits": data.info.bits_per_sample,
            "channels": data.info.channels,
            "sample_rate": data.info.sample_rate
        }

        # track and tracktotal can be a combined string eg: 4/20
        if '/' in data['TRCK'][0]:
            trackdata = data['TRCK'][0].split('/', 1)
            tracknumber = trackdata[0]
            tracktotal = trackdata[1]
        else:
            tracknumber = data['TRCK'][0]
            tracktotal = 0

        # Year could be in different keys
        if data.get("TORY") is not None:
            date = data['TORY'][0]
        elif data.get("TDRC") is not None:
            date = str(data['TDRC'][0])
        else:
            date = str(None)

        metadata = MetaData(
            artist = data['TPE1'][0] if 'TPE1' in data else str(None),
            album = data['TALB'][0] if 'TALB' in data else str(None),
            title = data['TIT2'][0] if 'TIT2' in data else str(None),
            date = date,
            tracknumber = tracknumber,
            totaltracks = tracktotal,
            label = data['TPUB'][0] if 'TPUB' in data else str(None),
            genre = data['TCON'][0] if 'TCON' in data else str(None),
            comment = str(None),
            info = info
        )

        return metadata
    
    if file['extension'] == 'mp3':
        data = MP3(file['location'], ID3=EasyID3)

        info = {
            "length": data.info.length,
            "bits": data.info.bitrate,
            "channels": data.info.channels,
            "sample_rate": data.info.sample_rate
        }

        # track and tracktotal can be a combined string eg: 4/20
        if '/' in data['tracknumber'][0]:
            trackdata = data['tracknumber'][0].split('/', 1)
            tracknumber = trackdata[0]
            tracktotal = trackdata[1]
        else:
            tracknumber = data['tracknumber'][0]
            tracktotal = 0

        metadata = MetaData(
            artist = data['artist'][0] if 'artist' in data else str(None),
            album = data['album'][0] if 'album' in data else str(None),
            title = data['title'][0] if 'title' in data else str(None),
            date = data['date'][0] if 'date' in data else str(None),
            tracknumber = tracknumber,
            totaltracks = tracktotal,
            label = data['label'][0] if 'label' in data else str(None),
            genre = data['genre'][0] if 'genre' in data else str(None),
            comment = data['comment'][0] if 'comment' in data else str(None),
            info = info
        )

        return metadata
    
    if file['extension'] == 'm4a':
        data = MP4(file['location'])

        info = {
            "length": data.info.length,
            "bits": data.info.bits_per_sample,
            "channels": data.info.channels,
            "sample_rate": data.info.sample_rate
        }

        metadata = MetaData(
            artist = data['\xa9ART'][0] if '\xa9ART' in data else str(None),
            album = data['\xa9alb'][0] if '\xa9alb' in data else str(None),
            title = data['\xa9nam'][0] if '\xa9nam' in data else str(None),
            date = data['\xa9day'][0] if '\xa9day' in data else str(None),
            tracknumber = data.get('trkn')[0][0] if 'trkn' in data else 0,
            totaltracks = data.get('trkn')[0][1] if 'trkn' in data else 0,
            label = data['TPUB'][0] if 'TPUB' in data else str(None),
            genre = data['\xa9gen'][0] if '\xa9gen' in data else str(None),
            comment = str(None),
            info = info
        )

        return metadata