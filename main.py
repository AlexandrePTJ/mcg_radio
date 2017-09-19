from mpd import MPDClient
import time

client = MPDClient()
client.connect('localhost', 6600)
while True:
    for song in client.playlistinfo():
        print(song)
    time.sleep(1)
client.disconnect()
