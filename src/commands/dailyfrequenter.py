import datetime
import logging

import discord
from discord import ApplicationContext, SlashCommandGroup, TextChannel
from discord.ext import commands, tasks

from core.bot import PathfinderBot
from core.frequenter_embed import generate_frequenter_embed
from core.path_picker import pick_paths


class DailyFrequenterCog(commands.Cog):
    dailyfrequenter_commands = SlashCommandGroup(
        "dailyfrequenter",
        "Manage the automatic daily frequenter",
        default_member_permissions=discord.Permissions(manage_guild=True),
    )

    def __init__(self, bot: PathfinderBot):
        self.bot: PathfinderBot = bot
        self.dailyfrequenter_task.start()

    def _build_dailyfrequenter_embed(self) -> discord.Embed:
        picked_paths = pick_paths()
        embed = generate_frequenter_embed(picked_paths)
        embed.title = f"Daily Frequenter for <t:{int(datetime.datetime.now().timestamp())}:d>"
        return embed

    @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
    async def dailyfrequenter_task(self):
        for guild_id in self.bot.sm.settings.guilds.keys():
            try:
                df = self.bot.sm.get_guild(int(guild_id)).get_dailyfrequenter()

                if not df.channel_id:
                    logging.warning(f"No channel configured for guild {guild_id}")
                    continue

                channel = self.bot.get_channel(df.channel_id)
                if not isinstance(channel, discord.TextChannel):
                    logging.warning(
                        f"Invalid or missing TextChannel {df.channel_id} in guild {guild_id}"
                    )
                    continue

                previous_message = None
                if df.message_id:
                    try:
                        previous_message = await channel.fetch_message(df.message_id)
                    except discord.NotFound:
                        logging.warning(f"Message {df.message_id} not found in guild {guild_id}")
                        previous_message = None
                    except discord.Forbidden:
                        logging.error(
                            f"No permission to fetch message {df.message_id} in guild {guild_id}"
                        )
                        continue
                    except discord.HTTPException as e:
                        logging.error(
                            f"HTTP error fetching message {df.message_id} in {guild_id}: {e}"
                        )
                        continue

                embed = self._build_dailyfrequenter_embed()

                if previous_message:
                    try:
                        await previous_message.edit(embed=embed)
                    except discord.NotFound:
                        logging.warning(
                            f"Message {df.message_id} disappeared while editing in {guild_id}"
                        )
                    except discord.Forbidden:
                        logging.error(
                            f"No permission to edit message {df.message_id} in guild {guild_id}"
                        )
                    except discord.HTTPException as e:
                        logging.error(
                            f"HTTP error editing message {df.message_id} in {guild_id}: {e}"
                        )
                else:
                    try:
                        await channel.send(embed=embed)
                        logging.info(f"Reposted dailyfrequenter in {guild_id}")
                    except discord.Forbidden:
                        logging.error(f"No permission to send message in {df.channel_id}")
                    except discord.HTTPException as e:
                        logging.error(f"HTTP error sending message in {guild_id}: {e}")

            except Exception as e:
                logging.exception(
                    f"Unexpected error in post_dailyfrequenter for guild {guild_id}: {e}"
                )

    @dailyfrequenter_task.before_loop
    async def before_post_dailyfrequenter(self):
        await self.bot.wait_until_ready()

    # ---------------------------------------------------------------------------- #
    #                             DAILYFREQUENTER VIEW                             #
    # ---------------------------------------------------------------------------- #
    @dailyfrequenter_commands.command(
        name="view", description="Show the current configuration and status of the daily frequenter"
    )
    async def view_dailyfrequenter(self, ctx: ApplicationContext):
        gsm = self.bot.sm.get_guild(ctx.guild.id)
        df = gsm.get_dailyfrequenter()

        if not df.channel_id:
            await ctx.respond("No daily frequenter is currently configured.", ephemeral=True)
            return

        channel = self.bot.get_channel(df.channel_id)
        if channel and isinstance(channel, TextChannel):
            await ctx.respond(
                f"Daily frequenter is currently set up in {channel.mention}.", ephemeral=True
            )
        else:
            await ctx.respond(
                f"Daily frequenter is currently set up in an unknown channel with ID {df.channel_id}.",
                ephemeral=True,
            )

    # ---------------------------------------------------------------------------- #
    #                             DAILYFREQUENTER SETUP                            #
    # ---------------------------------------------------------------------------- #
    @dailyfrequenter_commands.command(
        name="setup", description="Setup an automatic daily frequenter in this channel"
    )
    async def setup_dailyfrequenter(self, ctx: ApplicationContext):
        if not isinstance(ctx.channel, TextChannel):
            await ctx.respond(
                "This command must be used in a text channel I can access.",
                ephemeral=True,
            )
            return

        embed = self._build_dailyfrequenter_embed()

        try:
            message = await ctx.channel.send(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I don't have permission to send messages here.", ephemeral=True)
            return
        except discord.HTTPException as e:
            await ctx.respond(f"Failed to send message: {e}", ephemeral=True)
            return

        gsm = self.bot.sm.get_guild(ctx.guild.id)
        gsm.set_dailyfrequenter(ctx.channel.id, message.id)

        await ctx.respond(
            f"Daily frequenter successfully set up in {ctx.channel.mention}.",
            ephemeral=True,
        )

    # ---------------------------------------------------------------------------- #
    #                             DAILYFREQUENTER CLEAR                            #
    # ---------------------------------------------------------------------------- #
    @dailyfrequenter_commands.command(
        name="clear", description="Clear the automatic daily frequenter"
    )
    async def clear_dailyfrequenter(self, ctx: ApplicationContext):
        gsm = self.bot.sm.get_guild(ctx.guild.id)
        gsm.clear_guild()  # currently removes all guild-specific settings

        await ctx.respond(
            "Daily frequenter configuration cleared for this server.",
            ephemeral=True,
        )


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
def setup(bot):
    bot.add_cog(DailyFrequenterCog(bot))
