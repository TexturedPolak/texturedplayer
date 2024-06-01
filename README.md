# TexturedPlayer - ffplay and python based TUI music player
![](https://img.shields.io/github/license/TexturedPolak/texturedplayer?style=for-the-badge
)
![](https://img.shields.io/github/last-commit/TexturedPolak/texturedplayer?style=for-the-badge
)
![](https://img.shields.io/github/stars/TexturedPolak/texturedplayer?style=for-the-badge
)
![](https://img.shields.io/github/languages/top/TexturedPolak/texturedplayer?style=for-the-badge)
![](https://i.imgur.com/Ub561YH.png)
## Requirements:
- **ffplay** installed (it comes with **ffmpeg**). Search on google, how to install **ffmpeg** that on your OS.
- **[Textual](https://github.com/textualize/textual/)** library. You can install it using `pip install textual`.
## Optional
- **[Tinytag](https://github.com/devsnd/tinytag)** library for metadata (like title, author etc.) support. You can install it using `pip install tinytag`.
- **[Pypresence](https://github.com/qwertyquerty/pypresence)** library for discord rich presence (in-game status). You can install it using `pip install pypresence`
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
## Functions
- Create randomized playlist from files in chosen (in config.json) directory.
- Play any formats supported by ffplay.
## Usage
0. Clone this repository and install requirements.
1. Rename **sample_config.json** to **config.json**
2. Edit `music-directory` in **config.json**.
3. Run **main.py**
4. Enjoy :)

> [!WARNING]  
> `ffplay` can also play videos. This program however will just play sound from videos. **Put into music directory only music for the best expierence.**

> [!WARNING]  
> **Any none video or sound file in music directory can slow down player** except `playlist.json`.

> [!NOTE]  
> `playlist.json` will be created in music directory. That file store information about playlist. It will be ignored by `ffplay`.
