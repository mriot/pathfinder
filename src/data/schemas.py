from dataclasses import dataclass, field
from typing import Dict, List, Literal

# ---------------------------------------------------------------------------- #
#                                     TYPES                                    #
# ---------------------------------------------------------------------------- #
DungeonID = str
PathID = int

Blacklist = Dict[DungeonID, List[PathID]]


# ---------------------------------------------------------------------------- #
#                                   DATACLASSES                                #
# ---------------------------------------------------------------------------- #
@dataclass
class DailyFrequenter:
    channel_id: int | None = None
    message_id: int | None = None
    edit_last_message: bool = True  # False = del old + post new msg ## ! CURRENTLY UNUSED


@dataclass
class GuildSettings:
    dailyfrequenter: DailyFrequenter = field(default_factory=DailyFrequenter)


@dataclass
class UserSettings:
    blacklist: Blacklist = field(default_factory=dict)


@dataclass
class Settings:
    guilds: Dict[int, GuildSettings] = field(default_factory=dict)
    users: Dict[int, UserSettings] = field(default_factory=dict)


# ---------------------------------------------------------------------------- #
#                                 CORE STRUCTS                                 #
# ---------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Environment:
    TOKEN: str
    APP_ID: int
    DEBUG_GUILD_ID: int | None


@dataclass(frozen=True)
class DungeonPath:
    id: PathID
    name: str
    level: int
    time_of_day: Literal["Day", "Night"]
    story: bool


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
