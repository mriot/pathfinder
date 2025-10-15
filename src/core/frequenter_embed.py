import itertools
import random
from typing import List

import discord

from data.dungeons import DUNGEONS
from data.emojis import BotEmojis
from data.schemas import Candidate


def _tod_emoji(value: str) -> str:
    return BotEmojis.NIGHT_SIGIL if value.lower() == "night" else ""


def generate_frequenter_embed(picked_paths: List[Candidate]):
    dungeon_sections = []
    sorted_candidates = sorted(picked_paths, key=lambda x: x.dungeon_id)  # makes grouping easier
    for dungeon_id, group in itertools.groupby(sorted_candidates, key=lambda x: (x.dungeon_id)):
        dungeon = next(d for d in DUNGEONS if d.id == dungeon_id)
        paths = []

        for candidate in sorted(group, key=lambda x: x.path_id):
            path = next(p for p in dungeon.paths if p.id == candidate.path_id)
            paths.append(f"{path.name} {_tod_emoji(path.time_of_day)}")

        dungeon_sections.append(f"### {dungeon.emoji} {dungeon.name}" + "\n - ".join(["", *paths]))

    random.shuffle(dungeon_sections)
    embed = discord.Embed()
    embed.description = "\n".join(dungeon_sections)
    embed.set_footer(text=f"Generated {len(picked_paths)} paths for you. Enjoy!")

    return embed
