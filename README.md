# Telegram PlaylistAudioBot

## PlaylistAudioBot:

🇬🇧 Telegram playlist download bot with ytdl (m4a, only audio)

🇹🇷 Telegram oynatma listesi indirici bot (m4a, sadece ses)

Demo in Telegram: [@PlaylistAudioBot](https://t.me/PlaylistAudioBot)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/HuzunluArtemis/PlaylistAudioBot)

## Features
<details>
  <summary><b>Click Here For Details</b></summary><br>

- Youtube-DL downloading status
- Fully customizable progressbar
- Auto update ytdl with every request
- Only one process in same time (for stabilization)
- Embed thumbnail, metadata's to file
- Custom ytdl format selector (dont change if you dont know)
- Custom thumbnail (replace src/file.jpg with yours)
- Force Subscribe
- Video limit (give 0 for unlimited, default 0)
- Size limit (give 0 for unlimited, default 0)
- Logger, Pinger
</details>

## Setting up config file
<details>
    <summary><b>Click Here For Details</b></summary><br>
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
- `VIDEO_LIMIT`: Max video limit. Example: `3`, `62`, `52` (give 0 for unlimited, default 0)
- `VIDEO_LIMIT`: Max playlist size limit in bytes. (give 0 for unlimited, default 0)
- `UPDATE_YTDL_EVERY_DOWNLOAD`: Give `True` if you want to update ytdl in every download command. Default `True`
- `SLEEP_BETWEEN_SEND_FILES`: For floodwait. Leave blank if you dont know.
- `YTDL_DOWNLOAD_FORMAT`: Ytdl format selector. Leave blank if you dont know.
</details>

## License
<details>
    <summary><b>Click Here For Details</b></summary>
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
