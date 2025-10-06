import logging

import discord

from storage.settings_manager import SettingsManager


class PathfinderBot(discord.Bot):
    def __init__(self, settings_manager: SettingsManager, **kwargs):
        super().__init__(**kwargs)
        self.sm = settings_manager

    async def on_ready(self):
        logging.info(f"Logged in as {self.user}")
        await self.sync_commands()

    async def on_application_command(self, ctx):
        logging.info(
            f"{ctx.author} ({ctx.author.id}) used `/{ctx.command}` with options {ctx.selected_options}"
        )
