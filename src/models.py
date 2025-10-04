from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Literal

Blacklist = Dict[str, list[int]]


@dataclass
class UserSettings:
    blacklist: Blacklist = field(default_factory=dict)


# TODO
# @dataclass
# class GuildSettings:
#     users: Dict[str, UserSettings] = field(default_factory=dict)


@dataclass
class Settings:
    # guilds: Dict[str, GuildSettings] = field(default_factory=dict)
    users: Dict[str, UserSettings] = field(default_factory=dict)


@dataclass(frozen=True)
class Environment:
    token: str
    app_id: int
    guild_id: int | None
    root: Path


@dataclass(frozen=True)
class DungeonPath:
    id: int
    name: str
    level: int
    time_of_day: Literal["Day", "Night"]
    story: bool
    hidden: bool = False  # used for Arah Story as it's not repeatable


@dataclass(frozen=True)
class Dungeon:
    id: str
    name: str
    emoji: str
    paths: list[DungeonPath]


@dataclass(frozen=True)
class Candidate:
    dungeon_id: str
    path_id: int
