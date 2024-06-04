# TexturedPlayer - ffplay and python based TUI music player
<img src="https://i.imgur.com/xseHVj1.png" style="width:50px;"/>

![](https://img.shields.io/github/license/TexturedPolak/texturedplayer?style=for-the-badge
)
![](https://img.shields.io/github/last-commit/TexturedPolak/texturedplayer?style=for-the-badge
)
![](https://img.shields.io/github/stars/TexturedPolak/texturedplayer?style=for-the-badge
)
![](https://img.shields.io/github/languages/top/TexturedPolak/texturedplayer?style=for-the-badge)
![](https://i.imgur.com/jZflVR8.png)
## Requirements:
- **ffplay** installed (it comes with **ffmpeg**). Search on google, how to install **ffmpeg** that on your OS.
- **[Textual](https://github.com/textualize/textual/)** library. You can install it using `pip install textual`.
## Optional
- **[Tinytag](https://github.com/devsnd/tinytag)** library for metadata (like title, author etc.) support. You can install it using `pip install tinytag`.
- **[Pypresence](https://github.com/qwertyquerty/pypresence)** library for discord rich presence (in-game status). You can install it using `pip install pypresence`.<br>
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
> [!NOTE]  
> Songs in discord rich presence may change with a delay (about 15 seconds).
## Functions
- Create randomized playlist from files in chosen (in config.json) directory.
- Play any formats supported by ffplay.
## Instalation
Install it from [releases](https://github.com/TexturedPolak/texturedplayer) or clone this repository and install requirements.
## Usage
1. Rename **sample_config.json** to **config.json** (Windows only)
2. Edit `music-directory` in **config.json** (Windows) or **~/.texturedplayer/config.json** (Linux and MacOS).
3. Run **main.py** (Repo cloned) or **texturedplayer** (Installed only)
4. Enjoy :)

> [!WARNING]  
> `ffplay` can also play videos. This program however will just play sound from videos. **Put into music directory only music for the best expierence.**

> [!WARNING]  
> **Any none video or sound file in music directory can slow down player** except `playlist.json`.

> [!NOTE]  
> `playlist.json` will be created in music directory. That file store information about playlist. It will be ignored by `ffplay`.
