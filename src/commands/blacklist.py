from typing import List

import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.commands import option
from discord.ext import commands

from dungeons import DUNGEONS
from main import PathfinderBot


class Blacklist(commands.Cog):
    blacklist_commands = SlashCommandGroup("blacklist", "Manage your personal blacklist")

    @staticmethod
    def _path_id_autocomplete(ctx: ApplicationContext) -> List[discord.OptionChoice]:
        for d in DUNGEONS:
            if d.id == ctx.options.get("dungeon"):
                return [
                    discord.OptionChoice(name=p.name, value=p.id) for p in d.paths if not p.hidden
                ]
        return []

    def __init__(self, bot: PathfinderBot):
        self.bot: PathfinderBot = bot

    # ---------------------------------------------------------------------------- #
    #                                BLACKLIST VIEW                                #
    # ---------------------------------------------------------------------------- #
    @blacklist_commands.command(
        name="view", description="View your personal blacklist (only you can see this)"
    )
    async def show_blacklist(self, ctx: ApplicationContext):
        blacklist = self.bot.user_blacklist(ctx.author.id)

        lines = []
        for dungeon in DUNGEONS:
            blacklist_entry = blacklist.get(dungeon.id)
            if isinstance(blacklist_entry, list) and len(blacklist_entry) >= 4:
                lines.append(f"{dungeon.emoji} **{dungeon.name}**: All paths")
            elif isinstance(blacklist_entry, list) and blacklist_entry:
                paths = [("Story" if p == 0 else f"P{p}") for p in blacklist_entry]
                lines.append(f"{dungeon.emoji} **{dungeon.name}**: {', '.join(paths)}")

        embed = discord.Embed(title="Your current blacklist")
        embed.description = (
            "\n".join(lines) if len(lines) > 0 else "It's empty :face_holding_back_tears:"
        )
        embed.set_footer(text="Dungeons/Paths listed here won't be included in your routes")
        await ctx.respond(embed=embed, ephemeral=True)

    # ---------------------------------------------------------------------------- #
    #                                 BLACKLIST ADD                                #
    # ---------------------------------------------------------------------------- #
    @blacklist_commands.command(
        name="add", description="Exclude a dungeon or path from your routes"
    )
    @option(
        "dungeon",
        str,
        description="Dungeon to exclude",
        choices=[discord.OptionChoice(name=d.name, value=d.id) for d in DUNGEONS],
    )
    @option(
        "path",
        int,
        description="Path to exclude (optional)",
        autocomplete=_path_id_autocomplete,
    )
    async def exclude(self, ctx: ApplicationContext, dungeon: str, path: int | None = None):
        if path is not None and (path < 0 or path > 4):
            return await ctx.respond("Invalid path :face_with_raised_eyebrow:", ephemeral=True)

        user_settings = self.bot.sm.user_settings(ctx.author.id)
        selected_dungeon = next(d for d in DUNGEONS if d.id == dungeon)

        if dungeon not in user_settings.blacklist:
            user_settings.blacklist[dungeon] = []

        if path is not None:
            if path not in user_settings.blacklist[dungeon]:
                user_settings.blacklist[dungeon].append(path)
                user_settings.blacklist[dungeon].sort()
        else:
            user_settings.blacklist[dungeon] = [
                p.id for p in selected_dungeon.paths if not p.hidden
            ]

        self.bot.sm.mark_dirty()

        embed = discord.Embed(title="Blacklist updated")
        path_info = "All paths" if path is None else selected_dungeon.paths[path].name
        embed.description = (
            f"{selected_dungeon.emoji} **{selected_dungeon.name}**: {path_info} added to blacklist"
        )

        await ctx.respond(embed=embed, ephemeral=True)
        await self.show_blacklist(ctx)

    # ---------------------------------------------------------------------------- #
    #                               BLACKLIST REMOVE                               #
    # ---------------------------------------------------------------------------- #
    @blacklist_commands.command(
        name="remove", description="Remove a dungeon or path from your blacklist"
    )
    @option(
        "dungeon",
        str,
        description="Dungeon",
        choices=[discord.OptionChoice(name=d.name, value=d.id) for d in DUNGEONS],
    )
    @option(
        "path",
        int,
        description="Path (optional)",
        autocomplete=_path_id_autocomplete,
    )
    async def include(self, ctx: ApplicationContext, dungeon: str, path: int | None = None):
        if user_id := str(ctx.author.id):
            if user_id not in self.bot.sm.settings.users:
                return await ctx.respond("You have no blacklist entries.", ephemeral=True)

            user_settings = self.bot.sm.settings.users[user_id]
            selected_dungeon = next(d for d in DUNGEONS if d.id == dungeon)

            if dungeon in user_settings.blacklist:
                if path is not None:
                    user_settings.blacklist[dungeon].remove(path)
                    if len(user_settings.blacklist[dungeon]) == 0:
                        del user_settings.blacklist[dungeon]
                else:
                    del user_settings.blacklist[dungeon]

            self.bot.sm.mark_dirty()

        embed = discord.Embed(title="Blacklist updated")
        path_info = "All paths" if path is None else selected_dungeon.paths[path].name
        embed.description = f"{selected_dungeon.emoji} **{selected_dungeon.name}**: {path_info} removed from blacklist"

        await ctx.respond(embed=embed, ephemeral=True)
        await self.show_blacklist(ctx)

    # ---------------------------------------------------------------------------- #
    #                                BLACKLIST RESET                               #
    # ---------------------------------------------------------------------------- #
    @blacklist_commands.command(name="clear", description="Clear your personal blacklist")
    async def clear_blacklist(self, ctx: ApplicationContext):
        if user_id := str(ctx.author.id):
            if user_id in self.bot.sm.settings.users:
                self.bot.sm.settings.users[user_id].blacklist = {}
                self.bot.sm.mark_dirty()

        await ctx.respond("Cleared your personal blacklist", ephemeral=True)


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
def setup(bot):
    bot.add_cog(Blacklist(bot))
