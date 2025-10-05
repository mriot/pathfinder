import itertools
import logging
import random
from typing import List

import discord

from dungeons import DUNGEONS
from models import Blacklist, Candidate, Dungeon
from settings import SettingsManager
from utils import setup_env, setup_logging


# ---------------------------------------------------------------------------- #
#                                PATHFINDER BOT                                #
# ---------------------------------------------------------------------------- #
class PathfinderBot(discord.Bot):
    def __init__(self, settings_manager: SettingsManager, **kwargs):
        super().__init__(**kwargs)
        self.sm = settings_manager


# ---------------------------------------------------------------------------- #
#                                  PATH PICKER                                 #
# ---------------------------------------------------------------------------- #
def pick_paths(
    dungeons: List[Dungeon] = DUNGEONS,
    blacklist: Blacklist = {},
    path_count: int = 8,
    no_story: bool = False,
    time_of_day: str | None = None,
    ignore_filters: bool = False,
) -> List[Candidate]:
    if path_count <= 0:
        return []

    candidates: List[Candidate] = []

    for dungeon in dungeons:
        excluded = blacklist.get(dungeon.id)

        # TODO might be wrong?
        if not ignore_filters and excluded == []:
            continue  # entire dungeon excluded

        for path in dungeon.paths:
            if path.hidden:
                continue
            if not ignore_filters:
                if isinstance(excluded, list) and path.id in excluded:
                    continue
                if no_story and path.story:
                    continue
                if time_of_day and path.time_of_day.lower() != time_of_day.lower():
                    continue

            candidates.append(Candidate(dungeon.id, path.id))

    return random.sample(candidates, min(path_count, len(candidates)))


# ---------------------------------------------------------------------------- #
#                               FREQUENTER EMBED                               #
# ---------------------------------------------------------------------------- #
def _tod_emoji(value: str) -> str:
    return "<:night_sigil:1423998252705120390>" if value.lower() == "night" else ""


def generate_frequenter_embed(candidates: List[Candidate]):
    dungeon_sections = []
    sorted_candidates = sorted(candidates, key=lambda x: x.dungeon_id)  # makes grouping easier
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
    embed.set_footer(text=f"Generated {len(candidates)} paths for you. Enjoy!")

    return embed


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def main():
    setup_logging()
    env = setup_env()
    sm = SettingsManager()
    bot = PathfinderBot(
        intents=discord.Intents.default(),
        application_id=env.app_id,
        auto_sync_commands=True,
        debug_guilds=[env.guild_id] if env.guild_id else None,
        settings_manager=sm,
    )

    bot.load_extension("commands.frequenter")
    bot.load_extension("commands.blacklist")
    bot.load_extension("commands.dailyfrequenter")

    @bot.event
    async def on_ready():
        logging.info(f"Logged in as {bot.user}")
        await bot.sync_commands()

    @bot.listen("on_application_command")
    async def on_command(ctx):
        logging.info(
            f"{ctx.author} ({ctx.author.id}) used `/{ctx.command}` with options {ctx.selected_options}"
        )

    bot.run(env.token)


if __name__ == "__main__":
    main()
