import logging

import discord

from storage.settings_manager import SettingsManager


class PathfinderBot(discord.Bot):
    def __init__(self, settings_manager: SettingsManager, **kwargs):
        super().__init__(**kwargs)
        self.sm = settings_manager

    async def on_ready(self):
        logging.info(
            f"Logged in as {self.user} ({f'DEBUG MODE on {self.debug_guilds}' if self.debug_guilds else 'PROD MODE'})"
        )
        await self.sync_commands()

    async def on_application_command(self, ctx):
        logging.info(
            f"{ctx.author} ({ctx.author.id}) used `/{ctx.command}` with options {ctx.selected_options} in guild {ctx.guild.name} ({ctx.guild.id})"
        )

    async def on_guild_join(self, guild):
        logging.info(f"Joined guild: {guild.name} (ID: {guild.id})")

    async def on_guild_remove(self, guild):
        logging.info(f"Removed from guild: {guild.name} (ID: {guild.id})")
        self.sm.get_guild(guild.id).clear_guild()
