import eyed3
import urllib
import argparse
import time, yandex_music
from yandex_music.client import Client
from progress.bar import IncrementalBar

parser = argparse.ArgumentParser(description="download music of Yandex Music")
parser.add_argument('-u', '--user', help='is your username')
parser.add_argument('-p', '--pasw', help='is your password')
args = parser.parse_args()

client = Client.from_credentials(args.user, args.pasw)
tracklist = client.users_likes_tracks()

bar = IncrementalBar('Моя музыка', max = len(tracklist.tracks))

def down(w, filename):
    try:
        w.download(filename)
        return False
    except yandex_music.exceptions.NetworkError:
        time.sleep(10)
        print("reload hui")
        down(w, filename)
        return False
    except yandex_music.exceptions.Unauthorized:
        return True

def createNameTrack(w):
    filename = str(position)+"_"+ w.title +" album-"+ w.albums[0].title +" artist-"+ w.artists[0].name+ ".mp3"
    filename = filename.replace("/", "") \
        .replace("~", "") \
        .replace("%", "") \
        .replace("&", "") \
        .replace("*", "") \
        .replace("?", "") \
        .replace(":", "") \
        .replace("{", "") \
        .replace("}", "") \
        .replace("\\", "") \
        .replace("<", "") \
        .replace(">", "") \
        .replace("+", "") \
        .replace("|", "")
    return filename

def downloadTracks(w):
    filename = createNameTrack(w)
    if down(w, filename):
        print("hui wsw" + str(1))
    else:
        e = eyed3.load(filename)
        e.initTag()
        e.tag.artist = w.artists[0].name
        e.tag.album = w.albums[0].title
        e.tag.album_artist = w.albums[0].artists[0].name
        e.tag.title = w.title
        e.tag.track_num = 0
        e.tag.images.set(3, urllib.request.urlopen("https://" + w.cover_uri.replace("%%", "400x400")).read(), 'image/png')
        e.tag.save()
        print(w.title)
        print(w.artists[0].name)
        print(w.albums[0].title)
position = 0
try:
    for i in tracklist:
        bar.next()
        position+=1
        downloadTracks(i.track)

except KeyboardInterrupt:
    print("bye")
