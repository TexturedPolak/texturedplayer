#!/usr/bin/env python3

import datetime
import asyncio
from textual.worker import get_current_worker
# Playing music with vlc
import vlc

# Creating Playlists
import texturedplayer_utils

from textual_image.widget import Image
# TUI
try:
    from textual.app import App
    from textual.widgets import Button, Static, ProgressBar
    from textual.containers import Horizontal
    from textual import on
except ModuleNotFoundError:
    print("Textual is now still needed to run this app.")
    print("Install it with 'pip install textual'.")
    exit()
try:
    import vlc
except:
    print("python-vlc is now still needed to run this app.")
    print("Install it with 'pip install python-vlc'.")
    print("Make sure you have vlc installed as well.")
# Run in background
import subprocess
# Many things with os
import os
# For discord RPC
try:
    from pypresence import Presence
    from pypresence.types import ActivityType
    import time
    import multiprocessing
    discordRPC_enabled = True
except ModuleNotFoundError:
    discordRPC_enabled = False
from PIL import Image as PillowImage
# Init playlist and second process for playing music :)
newplaylist = texturedplayer_utils.get_newplaylist()
if os.name == "posix":
    proc = subprocess.Popen('echo "TexturedPlayer for Linux/MacOS"', shell=True, preexec_fn=os.setsid)
else:
    proc = subprocess.Popen('echo TexturedPlayer for Windows', shell=True)

# Define discordRPC loop
if discordRPC_enabled:
    def init_discordRPC(state,details,cover,album, start, stop):
        discordRPC = Presence('1246101303084585071') #Change if you want custom RPC ;)
        def connect():
            try:
                discordRPC.connect()
                return True
            except:
                return False
        connected = connect()
        while True:
            if connected:
                artist = None
                title = None
                if len(state.value.split("-")) >= 2:
                    title = state.value.split("-")[0]
                    artist = state.value.split("-")[1]
                else:
                    artist = state.value
                if album.value is None:
                    album_temp = album.value
                else:
                    album_temp = "Z albumu "+str(album.value)

                try:
                    if start.value != 0:
                        discordRPC.update(activity_type=ActivityType.LISTENING, state=artist, name=str(state.value), details=title, large_image=str(cover.value), small_image="texturedplayer-new", small_text="TexturedPlayer", large_text=album_temp, start=int(start.value), end=int(stop.value))
                    else:
                        discordRPC.update(activity_type=ActivityType.LISTENING, state=artist, name=str(state.value), details=title, large_image=str(cover.value), small_image="texturedplayer-new", small_text="TexturedPlayer", large_text=album_temp)
                except:
                    connected = connect()
            else:
                connected = connect()
            time.sleep(5)

# Is paused?
paused = False

def stop_vlc():
    global vlc_player
    vlc_player.stop()

# Main Class
class TexturMusic(App):
    # Style
    CSS = """
    Screen {
        layout: vertical;
        align: center middle;
    }
    
    .box {
        height: auto;
        border: heavy green;
        width: auto;
        text-align: center;
        align: center top;
        min-width: 75;
    }

    .buttons {
        min-width: 25;
    }

    Horizontal{
        width: auto;
        height: auto;
        padding: 1 0;
    }

    .big-button{
        height: auto;
        min-width: 37.5;
        text-align: center;
        align: center middle;
    }

    Image{
        width: 75;
        height: auto;
        text-align: center;
        align: center middle;
    }

    #eta{
        text-align: right;
        align: center top;
        width: 5;
    }

    ProgressBar{
        width: 70;
        text-align: center;
        align: center middle;
    }
    
    """

    # TUI
    def compose(self):
        """Create child widgets for the app."""
        
        self.cover_img = Image()
        self.cover_img.image =  PillowImage.new("RGB", (1024, 1024), "red")
        yield self.cover_img
        yield Static("Loading...", classes="box", id="song")
        with Horizontal():
            yield ProgressBar(show_eta=False)
            yield Static("00:00", id="eta")
        with Horizontal():
            yield Button("Previous", classes="buttons", id="previous")
            yield Button("Pause", classes="buttons", id="pause")
            yield Button("Next", classes="buttons", id="next")
        with Horizontal():
            yield Button("Reset playlist", classes='big-button', id="reset")
            yield Button("Quit", classes='big-button', id="quit")

            
    def change_text(self, change):
        song = self.query_one("#song")
        song.label = change
        song.update(change)
        song.refresh()


    # Main player
    async def play_next_song(self):
        #worker = get_current_worker()
        global proc
        global newplaylist
        global song_title
        # Global discordRPC current song
        if discordRPC_enabled:
            global current_song
            global current_cover
            global current_album
            global current_stop
            global current_start
        # Kill if music process is alive
        poll = proc.poll()
        if poll is None:
            await asyncio.to_thread(stop_vlc)
            await asyncio.sleep(0)
        # Play next song if exist
        if newplaylist["next"] < len(newplaylist["playlist"]):
            path = newplaylist["playlist"][newplaylist["next"]]
            newplaylist["next"] += 1
            if os.name == "posix":
                media = await asyncio.to_thread(vlc_instance.media_new, path)
                await asyncio.sleep(0)
                await asyncio.to_thread(vlc_player.set_media, media)
                await asyncio.sleep(0)
                vlc_player.play()
                
            song_title = await asyncio.to_thread(texturedplayer_utils.get_metadata, path)
            self.change_text(song_title)
            await asyncio.sleep(0)
            self.cover_img.image = await asyncio.to_thread(texturedplayer_utils.get_cover, path)
            await asyncio.sleep(0)
            
            # Change song in discord RPC (may display after 15 seconds)
            if discordRPC_enabled:
                current_song.value = song_title
                current_album.value = await asyncio.to_thread(texturedplayer_utils.get_album_name, path)
                await asyncio.sleep(0)
                temp_start = datetime.datetime.now()
                current_start.value = temp_start.timestamp()
                temp_stop = temp_start + datetime.timedelta(milliseconds=vlc_player.get_length())
                current_stop.value = temp_stop.timestamp()
                current_cover.value = await asyncio.to_thread(texturedplayer_utils.get_cover_url, path)
                await asyncio.sleep(0)
                
                
            
            await asyncio.to_thread(texturedplayer_utils.save_playlist, newplaylist)
            await asyncio.sleep(0)
        # Create new playlist, if next song don't exist
        else:
            newplaylist = await asyncio.to_thread(texturedplayer_utils.get_random_playlist, texturedplayer_utils.create_playlist())
            await asyncio.sleep(0)
            await self.play_next_song()

    # Next button
    @on(Button.Pressed, "#next")
    async def next_song(self):
        global paused
        global newplaylist
        if discordRPC_enabled:
            global current_state
            current_state.value = "Playing"
        #if paused:
            #newplaylist["next"] += 1
        paused = False


        if self.next_worker and not self.next_worker.is_finished:
            self.next_worker.cancel()

        # Start new worker
        self.next_worker = self.run_worker(
            self.play_next_song(),
            name="next_song_worker",
            exclusive=False  # allow replacement
        )
        #await self.play_next_song()
        
    # Previous button
    @on(Button.Pressed, "#previous")
    async def previous_song(self):
        global newplaylist
        global paused
        if discordRPC_enabled:
            global current_state
            current_state.value = "Playing"
        newplaylist["next"] -= 2
        if newplaylist["next"] < 0:
            newplaylist["next"] = 0
        paused = False

        if self.next_worker and not self.next_worker.is_finished:
            self.next_worker.cancel()

        # Start new worker
        self.next_worker = self.run_worker(
            self.play_next_song(),
            name="next_song_worker",
            exclusive=False  # allow replacement
        )
        
        #await self.play_next_song()
    
    # Pause button
    @on(Button.Pressed, "#pause")
    def pause_song(self):
        global newplaylist
        global paused
        global proc
        if discordRPC_enabled:
            global current_song
            global current_state
            global current_start
            global current_stop
        if paused is False:
            vlc_player.pause()
            self.change_text("Paused")
            if discordRPC_enabled:
                current_state.value = "Paused"
                current_start.value = 0
                current_stop.value = 0
            paused = True
            #newplaylist["next"]-=1
        else:
            if discordRPC_enabled:
                current_state.value = "Playing"
                temp_start = datetime.datetime.now() - datetime.timedelta(milliseconds=int(vlc_player.get_position()*vlc_player.get_length()))
                current_start.value = temp_start.timestamp()
                temp_stop = temp_start + datetime.timedelta(milliseconds=vlc_player.get_length())
                current_stop.value = temp_stop.timestamp()
            vlc_player.play()
            self.change_text(song_title)
            paused=False

    @on(Button.Pressed, '#quit')
    def quit(self):
        if discordRPC_enabled:
            discordRPC_loop.terminate()
        stop_vlc()
        exit()
    
    @on(Button.Pressed, '#reset')
    def reset_playlist(self):
        global newplaylist
        newplaylist = texturedplayer_utils.get_random_playlist(texturedplayer_utils.create_playlist())
        self.play_next_song()
            
    # Main Loop 
    # Needs to be fast!!
    async def main_loop(self):
        global proc
        global paused
        poll = proc.poll()
        #print(vlc_player.get_state())
        #print(vlc_player.get_length())
        if vlc_player.get_state() == vlc.State.Playing:
            self.query_one(ProgressBar).update(progress=vlc_player.get_position(), total=1)
            time_left_temp = datetime.timedelta(milliseconds=int(vlc_player.get_length() - (vlc_player.get_length() * vlc_player.get_position())))
            time_left = (datetime.datetime.min + time_left_temp).time()
            eta = self.query_one("#eta")
            eta.update(f"{time_left.minute:02d}:{time_left.second:02d}")
        if poll is not None and paused is False and vlc_player.get_state() == vlc.State.NothingSpecial or vlc_player.get_state() == vlc.State.Ended or vlc_player.get_state() == vlc.State.Error or vlc_player.get_length() == 0:
            await self.play_next_song()
    
    def on_mount(self) -> None:
        self.next_worker = None
        self.query_one(ProgressBar).update(progress=0, total=1)
        self.update_timer = self.set_interval(0.5, self.main_loop, pause=False)
    
# Running and exiting ;)
if __name__ == "__main__":
    # Start discord RPC loop
    if discordRPC_enabled:
        manager = multiprocessing.Manager()
        current_song = manager.Value('Idle', "Loading...")
        current_state = manager.Value("Idle2", "Playing")
        current_cover = manager.Value("cover", "texturedpolak")
        current_album = manager.Value("album", None)
        current_start = manager.Value("start", datetime.datetime.now().timestamp())
        current_stop = manager.Value("stop", datetime.datetime.now().timestamp())
        discordRPC_loop=multiprocessing.Process(target=init_discordRPC, args=(current_song, current_state, current_cover, current_album, current_start, current_stop))
        discordRPC_loop.start()
    song_title=""
    # Setup vlc
    vlc_instance = vlc.Instance()
    vlc_player = vlc_instance.media_player_new()
    def on_playing(event):
        subprocess.run(["notify-send", "TexturedPlayer", song_title])

    # Attach the event listener
    event_manager = vlc_player.event_manager()
    event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, on_playing)
    app = TexturMusic()
    app.run()
    if discordRPC_enabled:
        discordRPC_loop.terminate()
    stop_vlc()
