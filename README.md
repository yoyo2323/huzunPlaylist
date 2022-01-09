# Telegram PlaylistAudioBot

[![](https://img.shields.io/github/license/huzunluartemis/PlaylistAudioBot.svg?style=flat)](#)
[![](https://img.shields.io/github/issues-raw/huzunluartemis/PlaylistAudioBot.svg?style=flat)](#)
[![](https://img.shields.io/github/issues-closed-raw/huzunluartemis/PlaylistAudioBot.svg?style=flat)](#)
[![](https://img.shields.io/github/issues-pr-raw/huzunluartemis/PlaylistAudioBot.svg?style=flat)](#)
[![](https://img.shields.io/github/issues-pr-closed-raw/huzunluartemis/PlaylistAudioBot.svg?style=flat)](#)
[![](https://img.shields.io/github/languages/count/huzunluartemis/PlaylistAudioBot?style=flat)](#)
[![](https://img.shields.io/github/languages/top/huzunluartemis/PlaylistAudioBot?style=flat)](#)
[![](https://img.shields.io/github/last-commit/huzunluartemis/PlaylistAudioBot?style=flat)](#)
[![](https://img.shields.io/github/repo-size/huzunluartemis/PlaylistAudioBot.svg?style=flat)](#)
[![](https://img.shields.io/github/forks/huzunluartemis/PlaylistAudioBot?style=flat&logo=github)](#)
[![](https://img.shields.io/github/stars/huzunluartemis/PlaylistAudioBot?style=flat&logo=github)](#)
[![](https://img.shields.io/github/contributors-anon/HuzunluArtemis/PlaylistAudioBot?style=flat)](#)
[![](https://img.shields.io/github/watchers/huzunluartemis/PlaylistAudioBot?style=flat)](#)
[![](https://visitor-badge.laobi.icu/badge?page_id=huzunluartemis.PlaylistAudioBot)](#)
[![](https://img.shields.io/codacy/grade/ac102a243331444fa6e607f33de10066?style=flat)](#)
[![](https://img.shields.io/codefactor/grade/github/huzunluartemis/PlaylistAudioBot?style=flat)](#)
[![](https://img.shields.io/snyk/vulnerabilities/github/huzunluartemis/PlaylistAudioBot?style=flat)](#)
[![](https://img.shields.io/github/followers/huzunluartemis?logo=github&label=ha&style=flat)](#)
[![](https://img.shields.io/twitter/follow/huzunluartemis?&label=ha&color=blue&style=flat&logo=twitter)](https://twitter.com/HuzunluArtemis)
[![](https://img.shields.io/badge/dynamic/json?color=blue&label=ha&query=subscribers&url=https%3A%2F%2Fonline-users-api.up.railway.app%2Fcheck%3Fchat%3DHuzunluArtemis&logo=telegram)](https://t.me/HuzunluArtemis)
[![](https://img.shields.io/badge/website-up-blue?style=flat&logo=appveyor&style=flat&logo=twitter)](https://huzunluartemis.github.io/)
## PlaylistAudioBot:

🇬🇧 Telegram playlist download bot with ytdl (m4a, only audio)

🇹🇷 Telegram oynatma listesi indirici bot (m4a, sadece ses)

🔥 Demo in Telegram: [@PlaylistAudioBot](https://t.me/PlaylistAudioBot)

## Features
<details>
  <summary><b>🇬🇧 Click Here 🇹🇷 Buraya Tıkla</b></summary><br>

- Youtube-DL downloading status
- Fully customizable progressbar
- Auto update ytdl with every download
- Auto update all requirements with restart
- Only one process in same time (for stabilization)
- Embed thumbnail, metadata's to file
- Custom ytdl format selector (dont change if you dont know)
- Custom thumbnail (replace src/file.jpg with yours)
- Force Subscribe
- 2 type of user: Standart, Premium
- Video limit
- Size limit
- Quee
- Logger
- Shell
- Stats
- Restart
- Pinger
</details>

## Setting up config file
<details>
    <summary><b>🇬🇧 Click Here 🇹🇷 Buraya Tıkla</b></summary><br>
    <b>Required Variables:</b><br><br>
    
- `BOT_TOKEN`: Telegram Bot Token. Example: `3asd2a2sd32:As56das65d2as:ASd2a6s3d26as`
- `APP_ID`: Telegram App ID. Example: `32523453`
- `API_HASH`: Telegram Api Hash. Example: `asdasdas6d265asd26asd6as1das`
- `AUTH_IDS`: Auth only some groups or users. If you want public, leave it empty or give `0`. Example: `-100656 56191 -10056561`
- `BOT_USERNAME`: Your bot's username. without @. Example: `PlaylistAudioBot`

<b>Not Required Variables:</b>

- `OWNER_ID`: Bot's owner id. Send `/id` to `t.me/MissRose_bot` in private to get your id. Required for shell and say hello in every restart to you. If you don't want, leave it empty.
- `FORCE_SUBSCRIBE_CHANNEL`: Force subscribe channel or group. Example: `-1001327202752` or `@HuzunluArtemis`. To disable leave it empty. Do not forget to make admin your bot in forcesub channel or group.
- `CHANNEL_OR_CONTACT`: Your bot's channel or contact username. Example: `HuzunluArtemis`
- `JOIN_CHANNEL_STR`: Join channel warning string. See `config.py`.
- `YOU_ARE_BANNED_STR`: Banned user string. See `config.py`.
- `JOIN_BUTTON_STR`: Join button string. See `config.py`.
- `SORT_UPLOAD`: Sort files before upload. `ContentModification` or `normalsort` or `MetadataChange` or `naturalsort` or `reversesort`. Leave blank for playlist original sorting.
- `VIDEO_LIMIT`: Max video limit. Example: `3`, `62`, `52` (give 0 for unlimited, default 0)
- `VIDEO_LIMIT`: Max playlist size limit in bytes. (give 0 for unlimited, default 0)
- `UPDATE_YTDL_EVERY_DOWNLOAD`: Give `True` if you want to update ytdl in every download command. Default `True`
- `UPDATE_REQUIREMETS_EVERY_RESTART`: Give `True` if you want to update all requirements when restart. Default `True`
- `SLEEP_BETWEEN_SEND_FILES`: For floodwait. Leave blank if you dont know.
- `YTDL_DOWNLOAD_FORMAT`: Ytdl format selector. Leave blank if you dont know.
- `SEND_LOGS_WHEN_DYING`: Send log.txt while exiting. Default `False`
- `PREMIUM_USERS`: Premium user id's. Example: `100656 56191 50056561`
- `VIDEO_LIMIT_FREE_USER`: 0: Unlimited. Default `False`
- `VIDEO_LIMIT_PREMIUM_USER`: 0: Unlimited. Default `0`
- `SIZE_LIMIT_FREE_USER`: 0: Unlimited. Default `0`
- `SIZE_LIMIT_PREMIUM_USER`: 0: Unlimited. Default `0`
- `PROCESS_PER_USER_FREE_USER`: 0: Unlimited. Default `2`
- `PROCESS_PER_USER_PREMIUM_USER`: 0: Unlimited. Default `0`
</details>

## Deploy
<details>
  <summary><b>🇬🇧 Click Here 🇹🇷 Buraya Tıkla</b></summary><br>

<b>Deploy to Heroku:</b>

- [Open me in new tab](https://heroku.com/deploy?template=https://github.com/HuzunluArtemis/PlaylistAudioBot)
- Fill required variables
- Fill app name (or dismiss)
- Make you sure building with Dockerfile (as container. not heroku-18 or heroku-20)

<b>Deploy to Local:</b>

- install [python](https://www.python.org/downloads/) and [ffmpeg](https://www.ffmpeg.org/download.html) to your machine
- `git clone https://github.com/HuzunluArtemis/PlaylistAudioBot`
- `cd PlaylistAudioBot`
- `pip install -r requirements.txt`
- `python bot.py`

<b>Deploy to Vps:</b>

- `git clone https://github.com/HuzunluArtemis/PlaylistAudioBot`
- `cd PlaylistAudioBot`
- For Debian based distros `sudo apt install python3 && sudo snap install docker`
- For Arch and it's derivatives: `sudo pacman -S docker python`

</details>

## License
<details>
    <summary><b>🇬🇧 Click Here 🇹🇷 Buraya Tıkla</b></summary>
  <br>
  <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">
  <img src="https://www.gnu.org/graphics/gplv3-127x51.png" alt="GNU GPLv3 Image">
</a>
<br>
<br>
PlaylistAudioBot is Free Software: You can use, study share and improve it at your
will. Specifically you can redistribute and/or modify it under the terms of the 
  <a href="https://www.gnu.org/licenses/gpl.html">GNU General Public License</a> 
  as published by the Free Software Foundation, either version 3 of the License, 
  or (at your option) any later version.
</details>
