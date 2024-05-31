# Creating Playlists
import utils
# TUI
try:
    from textual.app import App, ComposeResult
    from textual.widgets import Button, Static
    from textual.containers import Horizontal
    from textual import on
except ModuleNotFoundError:
    print("Textual is now still needed to run this app.")
    print("Install it with 'pip install textual'.")
    exit()
# Run in background
import subprocess
# Many things with os
import os
import signal

# Init playlist and second process for playing music :)
newplaylist = utils.get_newplaylist()
if os.name == "posix":
    proc = subprocess.Popen('echo "TexturedPlayer for Linux/MacOS"', shell=True, preexec_fn=os.setsid)
else:
    proc = subprocess.Popen('echo TexturedPlayer for Windows', shell=True)


#Main Class
class TexturMusic(App):
    # Style
    CSS = """
    Screen {
        layout: vertical;
        align: center middle;
        
    }

    .box {
        height: auto;
        border: solid green;
        width: auto;
        text-align: center;
        align: center middle;
        min-width: 50;
    }
    .buttons {
        min-width: 25;
    }
    Horizontal{
        width: auto;
    }
    """

    # TUI
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Static("Loading...", classes="box", id="song")
        with Horizontal():
            yield Button("Previous", classes="buttons", id="previous")
            yield Button("Next", classes="buttons", id="next")
        
    def change_text(self, change):
        song = self.query_one("#song")
        song.label = change
        song.update(change)
        song.refresh()


    # Main player
    def play_next_song(self):
        global proc
        global newplaylist
        poll = proc.poll()
        if poll is not None:
            self.change_text("dead")
            #thread = threading.Thread(target=musicplayer.play_song,args=(playlist[0],))
            if newplaylist["next"] <= len(newplaylist["playlist"]):
                if os.name == "posix":
                    proc = subprocess.Popen(f'ffplay -nodisp -autoexit -af "volume=0.4" "{newplaylist["playlist"][newplaylist["next"]]}"',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT, 
                        shell=True, preexec_fn=os.setsid)
                else:
                    proc = subprocess.Popen(f'ffplay -nodisp -autoexit -af "volume=0.4" "{newplaylist["playlist"][newplaylist["next"]]}"',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT, 
                       shell=True)
                self.change_text(str(utils.get_metadata(newplaylist["playlist"][newplaylist["next"]])))
                newplaylist["next"] += 1
                utils.save_playlist(newplaylist)
            else:
                newplaylist = utils.get_random_playlist(utils.create_playlist())
                self.play_next_song()
        else:
            if os.name == "posix":
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            else:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT, 
                       shell=True)
            self.play_next_song()

    # Next button
    @on(Button.Pressed, "#next")
    def next_song(self):
        self.play_next_song()
        
    # Previous button
    @on(Button.Pressed, "#previous")
    def previous_song(self):
        global newplaylist
        newplaylist["next"] -= 2
        if newplaylist["next"] < 0:
            newplaylist["next"] = 0
        self.play_next_song()
        
            
    # Main Loop 
    # Needs to be fast!!
    def main_loop(self):
        global proc
        poll = proc.poll()
        if poll is not None:
            self.play_next_song()
    
    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1, self.main_loop, pause=False)
    
# Running and exiting ;)
if __name__ == "__main__":
    app = TexturMusic()
    app.run()
    if os.name == "posix":
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    else:
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT, 
                       shell=True)