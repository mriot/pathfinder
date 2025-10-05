from dataclasses import dataclass, field
from datetime import time
from pathlib import Path
from typing import Dict, List, Literal

# ---------------------------------------------------------------------------- #
#                                     TYPES                                    #
# ---------------------------------------------------------------------------- #
DungeonID = str
PathID = int

GuildID = str
UserID = str

Blacklist = Dict[DungeonID, List[PathID]]


# ---------------------------------------------------------------------------- #
#                                   DATACLASSES                                #
# ---------------------------------------------------------------------------- #
@dataclass
class DailyFrequenter:
    channel_id: int
    replace_last_message: bool = True
    time_for_post: time = time(0, 0)


@dataclass
class GuildSettings:
    dailyfrequenter: DailyFrequenter | None = None


@dataclass
class UserSettings:
    blacklist: Blacklist = field(default_factory=Blacklist)


@dataclass
class Settings:
    guilds: Dict[GuildID, GuildSettings] = field(default_factory=dict)
    users: Dict[UserID, UserSettings] = field(default_factory=dict)


# ---------------------------------------------------------------------------- #
#                                 CORE STRUCTS                                 #
# ---------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Environment:
    token: str
    app_id: int
    guild_id: int | None
    root: Path


@dataclass(frozen=True)
class DungeonPath:
    id: PathID
    name: str
    level: int
    time_of_day: Literal["Day", "Night"]
    story: bool
    hidden: bool = False  # used for Arah Story as it's not repeatable


@dataclass(frozen=True)
class Dungeon:
    id: DungeonID
    name: str
    emoji: str
    paths: list[DungeonPath]


@dataclass(frozen=True)
class Candidate:
    dungeon_id: DungeonID
    path_id: PathID
