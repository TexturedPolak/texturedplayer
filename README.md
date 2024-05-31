# TexturedPlayer - ffplay and python based music player

## Requirements:
- **ffplay** installed (it comes with **ffmpeg**). Search on google, how to install **ffmpeg** that on your OS.
- **[Textual](https://github.com/textualize/textual/)** library. You can install it using `pip install textual`.
## Optional
- **[Tinytag](https://github.com/devsnd/tinytag)** library for metadata (like title, author etc.) support.
## Functions
- Create randomized playlist from files in chosen (in config.json) directory.
- Play any formats supported by ffplay.
## Usage
0. Clone this repository and install requirements.
1. Edit `music-directory` in **config.json**.
2. Run **main.py**
3. Enjoy :)

> [!WARNING]  
> `ffplay` can also play videos. This program however will just play sound from videos. **Put into music directory only music for the best expierence.**

> [!NOTE]  
> `playlist.json` will be created in music directory. That file store information about playlist. It will be ignored by `ffplay`.
