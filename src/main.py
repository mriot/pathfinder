import logging
import random
from typing import List

import discord

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

    def user_blacklist(self, user_id: int) -> Blacklist:
        if user_settings := self.sm.settings.users.get(str(user_id), None):
            return user_settings.blacklist or {}
        return {}


# ---------------------------------------------------------------------------- #
#                                  PATH PICKER                                 #
# ---------------------------------------------------------------------------- #
def pick_paths(
    dungeons: List[Dungeon],
    blacklist: Blacklist,
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
