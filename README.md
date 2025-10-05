<h1 align="center">
    <sub>
      <img width="128" height="128" alt="061d1669-2556-4582-bc7d-1fba44de2c12 (Custom)" src="https://github.com/user-attachments/assets/ec8e9d7e-08f6-443d-997f-f8bf9474990d" />
    </sub>
    <br>
    Pathfinder
</h1>

<p align="center">
  A Guild Wars 2 Discord bot that randomizes your dungeon frequenter routes on demand
</p>

> [!WARNING]
> This project is still in development. Functionality is largely stable, but small bugs and refactoring may occur.  

## Usage

Autocomplete is available for all commands. Just start typing and you'll see the options available.

### 🎲 Generate Routes

Use `/frequenter` to create a randomized dungeon route.  
Optional filters let you control how paths are chosen.

#### Aliases

- `/nightfrequenter` → only night time dungeons  
- `/dayfrequenter` → only day time dungeons  
- `/chaosfrequenter` → ignores blacklist and filters  

---

### 🚫 Manage Your Blacklist

Keep certain dungeons or paths out of your generated routes.

> All blacklist commands are visible only to you

| Command             | Description                        |
| ------------------- | ---------------------------------- |
| `/blacklist view`   | Shows your personal blacklist      |
| `/blacklist add`    | Exclude a dungeon or specific path |
| `/blacklist remove` | Re-include a dungeon or path       |
| `/blacklist clear`  | Reset your entire blacklist        |

---

> [!NOTE]
> Blacklist data is saved per user. Clearing or adding entries only affects your own routes.


## Dev & Hosting

> Python 3.12

### .env

>[!IMPORTANT]
> Omit `GUILD_ID` in production

Create the `.env` file in the project's root directory.

``` ini
TOKEN=1234567890.1234567890.1234567890
APP_ID=1234567890
GUILD_ID=1234567890 # debug guild
```

### Service

> [!NOTE]
> I'm using [UV](https://docs.astral.sh/uv/) to run the bot.

- `sudo nano /etc/systemd/system/pathfinder.service`
- `sudo systemctl enable pathfinder.service`
- `sudo systemctl start pathfinder.service`

``` ini
[Unit]
Description=Pathfinder Discord Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/pathfinder
ExecStart=/root/.local/bin/uv run /root/pathfinder/src/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Data stored

Used for settings only.

- Guild (server) IDs
- User IDs

## Credits

- Thank you Devin for the bot idea.
- Thank you Everless for the `/chaosfrequenter` concept.
- Thank you Bird for testing the bot _("I have the urge to break things")_
