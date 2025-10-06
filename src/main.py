import discord

from core.bot import PathfinderBot
from storage.settings_manager import SettingsManager
from utils import setup_env, setup_logging


def main():
    setup_logging()
    env = setup_env()
    sm = SettingsManager()
    bot = PathfinderBot(
        intents=discord.Intents.default(),
        application_id=env.APP_ID,
        auto_sync_commands=True,
        debug_guilds=[env.DEBUG_GUILD_ID] if env.DEBUG_GUILD_ID else None,
        settings_manager=sm,
    )

    bot.load_extension("commands.frequenter")
    bot.load_extension("commands.blacklist")
    bot.load_extension("commands.dailyfrequenter")

    bot.run(env.TOKEN)


if __name__ == "__main__":
    main()
