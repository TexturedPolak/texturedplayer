# For files
import json
import os
# For one message ;)
from subprocess import Popen
import base64
import requests
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


from PIL import Image
import io

def resize_to_1024(image_bytes):
    # Normalize input to PIL Image
    if isinstance(image_bytes, Image.Image):
        img = image_bytes
    elif isinstance(image_bytes, io.BytesIO):
        img = Image.open(image_bytes)
    elif isinstance(image_bytes, (bytes, bytearray)):
        img = Image.open(io.BytesIO(image_bytes))
    else:
        raise TypeError(f"Unsupported type: {type(image_bytes)}")

    # Obliczamy skalę tak, aby obraz miał max 1024 px w obu wymiarach
    scale = 1024 / max(img.width, img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)

    # Skalowanie w górę lub w dół
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Tworzymy kwadrat 1024x1024
    new_img = Image.new("RGB", (1024, 1024), (0, 0, 0))

    # Centrowanie
    x = (1024 - new_w) // 2
    y = (1024 - new_h) // 2
    new_img.paste(img, (x, y))

    # Zapis do bajtów
    output = io.BytesIO()
    new_img.save(output, format="JPEG", quality=95)
    return output.getvalue()

def upload_catbox(image_bytes, filename="image.jpg"):
    url = "https://catbox.moe/user/api.php"
    data = {
        "reqtype": "fileupload",
    }
    files = {
        "fileToUpload": (filename, image_bytes)
    }

    r = requests.post(url, data=data, files=files)
    r.raise_for_status()
    return r.text.strip()
    
def get_cover_url(song_file: str) -> str:
    if tinytag_enabled is True:
        try:
            song_data = TinyTag.get(song_file, image=True)
        except:
            return "texturedplayer-new"
        print(get_cover(song_file=song_file))
        try:
            url = upload_catbox(resize_to_1024(get_cover(song_file=song_file)))
        except:
            url = "texturedplayer-new"
        print(url)
        return url
    
def get_cover(song_file:str):
    if tinytag_enabled is True:
        try:
            song_data = TinyTag.get(song_file, image=True)
        except:

            return Image.new("RGB", (1024, 1024), "#121212")
        try:
            if song_data.images.front_cover is not None:
                return io.BytesIO(song_data.images.front_cover.data)
            elif song_data.images.media is not None:
                return io.BytesIO(song_data.images.media.data)
            elif song_data.images.other is not None:
                return io.BytesIO(song_data.images.other.get("generic")[0].data)
            else:
                return Image.new("RGB", (1024, 1024), "#121212")
        except:
            print(":(")
            print(song_data.images.other)
            return Image.new("RGB", (1024, 1024), "#121212")
            


def get_album_name(song_file: str):
    if tinytag_enabled is True:
        try:
            song_data = TinyTag.get(song_file)
        except:
            return None
        if song_data.album is None:
            return None
        else:
            return str(song_data.album)
    else:
        return None

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
