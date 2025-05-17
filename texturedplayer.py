#!/usr/bin/env python3

# Playing music with vlc
import vlc

# Creating Playlists
import texturedplayer_utils
# TUI
try:
    from textual.app import App
    from textual.widgets import Button, Static
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
import signal
# For discord RPC
try:
    from pypresence import Presence
    import time
    import multiprocessing
    discordRPC_enabled = True
except ModuleNotFoundError:
    discordRPC_enabled = False
import asyncio

# Init playlist and second process for playing music :)
newplaylist = texturedplayer_utils.get_newplaylist()
if os.name == "posix":
    proc = subprocess.Popen('echo "TexturedPlayer for Linux/MacOS"', shell=True, preexec_fn=os.setsid)
else:
    proc = subprocess.Popen('echo TexturedPlayer for Windows', shell=True)

# Define discordRPC loop
if discordRPC_enabled:
    def init_discordRPC(state,details):
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
                try:
                    discordRPC.update(state=str(state.value), details=str(details.value),small_image='texturedplayer',small_text="TexturedPlayer",buttons=[{"label":"Check it out on Github! :)","url":"https://github.com/TexturedPolak/texturedplayer"}])
                except:
                    connected = connect()
            else:
                connected = connect()
            time.sleep(15)

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
    """

    # TUI
    def compose(self):
        """Create child widgets for the app."""
        yield Static("Loading...", classes="box", id="song")
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
    def play_next_song(self):
        global proc
        global newplaylist
        global song_title
        # Global discordRPC current song
        if discordRPC_enabled:
            global current_song
        # Kill if music process is alive
        poll = proc.poll()
        if poll is None:
            stop_vlc()
        # Play next song if exist
        if newplaylist["next"] < len(newplaylist["playlist"]):
            if os.name == "posix":
                pass
                song_title = str(texturedplayer_utils.get_metadata(newplaylist["playlist"][newplaylist["next"]]))
                media = vlc_instance.media_new(newplaylist["playlist"][newplaylist["next"]])
                vlc_player.set_media(media)
                vlc_player.play()
            
            self.change_text(str(texturedplayer_utils.get_metadata(newplaylist["playlist"][newplaylist["next"]])))
            # Change song in discord RPC (may display after 15 seconds)
            if discordRPC_enabled:
                current_song.value = str(texturedplayer_utils.get_metadata(newplaylist["playlist"][newplaylist["next"]]))
            newplaylist["next"] += 1
            texturedplayer_utils.save_playlist(newplaylist)
        # Create new playlist, if next song don't exist
        else:
            newplaylist = texturedplayer_utils.get_random_playlist(texturedplayer_utils.create_playlist())
            self.play_next_song()

    # Next button
    @on(Button.Pressed, "#next")
    def next_song(self):
        global paused
        global newplaylist
        if discordRPC_enabled:
            global current_state
            current_state.value = "Playing"
        if paused:
            newplaylist["next"] += 1
        paused = False
        self.play_next_song()
        
    # Previous button
    @on(Button.Pressed, "#previous")
    def previous_song(self):
        global newplaylist
        global paused
        if discordRPC_enabled:
            global current_state
            current_state.value = "Playing"
        if paused:
            newplaylist["next"] -= 1
        else:
            newplaylist["next"] -= 2
        if newplaylist["next"] < 0:
            newplaylist["next"] = 0
        paused = False
        self.play_next_song()
    
    # Pause button
    @on(Button.Pressed, "#pause")
    def pause_song(self):
        global newplaylist
        global paused
        global proc
        if discordRPC_enabled:
            global current_song
            global current_state
        if paused is False:
            vlc_player.pause()
            self.change_text("Paused")
            if discordRPC_enabled:
                current_state.value = "Paused"
                current_song.value = ":("
            paused = True
            newplaylist["next"]-=1
        else:
            if discordRPC_enabled:
                current_state.value = "Playing"
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
    def main_loop(self):
        global proc
        global paused
        poll = proc.poll()
        if poll is not None and paused is False and vlc_player.get_state() == vlc.State.NothingSpecial or vlc_player.get_state() == vlc.State.Ended:
            self.play_next_song()
    
    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1, self.main_loop, pause=False)
    
# Running and exiting ;)
if __name__ == "__main__":
    # Start discord RPC loop
    if discordRPC_enabled:
        manager = multiprocessing.Manager()
        current_song = manager.Value('Idle', "Loading...")
        current_state = manager.Value("Idle2", "Playing")
        discordRPC_loop=multiprocessing.Process(target=init_discordRPC, args=(current_song, current_state))
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
