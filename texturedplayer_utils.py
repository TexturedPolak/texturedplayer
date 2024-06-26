# For files
import json
import os
# For one message ;)
from subprocess import Popen
# For metadata
try:
    from tinytag import TinyTag
    tinytag_enabled=True
except ModuleNotFoundError:
    tinytag_enabled=False
    if os.name == "posix":
        proc = Popen('echo "Tinytag library is needed, if you want display metadata like title.\nInstall it using ~ pip install tinytag ~"', shell=True)
    else:
        proc = Popen('echo Tinytag library is needed, if you want display metadata like title.\nInstall it using ~ pip install tinytag ~', shell=True)
# For Random Playlist
import random
# Get music directory from config.json
try:
    if os.name == "posix":
        if os.path.exists(os.path.expanduser('~')+"/.texturedplayer/config.json"):
            music_directory = json.loads(open(os.path.expanduser('~')+"/.texturedplayer/config.json","r").read()).get("music-directory")
        else:
            if not os.path.exists(os.path.expanduser('~')+"/.texturedplayer"):
                os.mkdir(os.path.expanduser('~')+"/.texturedplayer/")
            open(os.path.expanduser('~')+"/.texturedplayer/config.json","w").write('{\n\t"music-directory":""\n}')
            print("Set your music directory in ~/.texturedplayer/config.json")
            exit()
    else:
        music_directory = json.loads(open("config.json","r").read()).get("music-directory")
except FileNotFoundError:
    print("No config.json file found! Download sample_config.json and rename it to config.json!")
    exit()
if music_directory is not None:
    try:
        os.chdir(music_directory)
    except FileNotFoundError:
        if os.name == "posix":
            print("Change music directory in ~/.texturedplayer/config.json")
        else:
            print("Change music directory in config.json")
        exit()
else:
    print("Broken config.json file.")
    exit()

# Functions :)

# Saves playlist to playlist.json file.
def save_playlist(playlist):
    file = open("playlist.json", "w")
    file.write(json.dumps(playlist))
    file.close()

# Randomize playlist.
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

# Create new playlist.
def create_playlist():
    playlist = []
    for file in os.listdir():
        if file != "playlist.json":
            playlist.append(file)
    newplaylist = {"playlist":playlist,"next":0}
    return newplaylist

# Get song metadata. If not have metadata, just return filename.
def get_metadata(song_file: str):
    if tinytag_enabled is True:
        try:
            song_data = TinyTag.get(song_file)
        except:
            return(song_file)
        if song_data.artist is None:
            return(song_file)
        else:
            return str(song_data.title) + " - " + str(song_data.artist)
    else:
        return(song_file)

# Get old playlist from playlist.json.
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
