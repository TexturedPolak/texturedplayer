# For files
import json
import os
# For sleep
import time
# For play music
import subprocess
# For tags
from tinytag import TinyTag
# For Random Playlist
import random
# Directory with music :)
music_directory = "/home/rafal/Pulpit/muzyka good/"
os.chdir(music_directory)

# Functions


def save_playlist(playlist):
    file = open("playlist.json", "w")
    file.write(json.dumps(playlist))
    file.close()


def get_random_playlist(newplaylist):
    playlist = newplaylist["playlist"]
    to_random = []
    for i in range(len(playlist)):
        to_random.append(i)
    randomized = []
    for i in range(len(to_random)):
        random_number = random.choice(to_random)
        to_random.remove(random_number)
        randomized.append(random_number)
    random_playlist = []
    for i in randomized:
        random_playlist.append(playlist[i])
    random_newplaylist = {"playlist":random_playlist,"next":newplaylist["next"]}
    return random_newplaylist


def create_playlist():

    playlist = []
    for file in os.listdir():
        if file != "playlist.json":
            playlist.append(file)
    newplaylist = {"playlist":playlist,"next":0}
    return newplaylist

def get_metadata(song_file: str):
    song_data = TinyTag.get(song_file)
    if song_data.artist is None:
        toreturn=song_file
    else:
        toreturn=str(song_data.title) + " - " + str(song_data.artist)
    return toreturn
    
def play_song(song_file: str):
    #song_data = TinyTag.get(song_file)
    #print(f"Playing {song_data.title} by {song_data.artist}")
    #subprocess.call(["ffplay", "-nodisp", "-autoexit", "-hide_banner", '-af', "volume=1", '-loglevel', 'quiet', song_file])
    os.system(f"ffplay -nodisp -autoexit -hide_banner -af -volume-0.1 -loglevel quiet {song_file}")
    #time.sleep(1)


def get_newplaylist():
    if os.path.exists("playlist.json"):
        newplaylist = json.loads(open("playlist.json","r").read())
        if newplaylist.get("playlist") is None or newplaylist.get("playlist") is []:
            newplaylist = get_random_playlist(create_playlist())
            save_playlist(newplaylist)
    else:
        newplaylist = get_random_playlist(create_playlist())
        save_playlist(newplaylist)
    
    return newplaylist

    #while True:
        #for song in playlist:

            #playlist.remove(song)
            #save_playlist(playlist)
            #play_song(song)

        #playlist = get_random_playlist(create_playlist())
        #save_playlist(playlist)


# Main loop
#play_playlist()
