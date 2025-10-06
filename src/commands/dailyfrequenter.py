import logging

from discord import (
    ApplicationContext,
    AutocompleteContext,
    OptionChoice,
    SlashCommandGroup,
    TextChannel,
    option,
)
from discord.ext import commands, tasks

from main import PathfinderBot, generate_frequenter_embed, pick_paths


class DailyFrequenterCog(commands.Cog):
    dailyfrequenter_commands = SlashCommandGroup(
        "dailyfrequenter", "Manage the automatic daily frequenter"
    )

    @staticmethod
    def _channel_autocomplete(ctx: AutocompleteContext):
        guild = ctx.interaction.guild
        user = ctx.bot.user
        if guild is None or user is None:
            return []

        member = guild.get_member(user.id)
        if member is None:
            return []

        return [
            OptionChoice(name=c.name, value=str(c.id))
            for c in guild.channels
            if c.name.lower().startswith(ctx.value.lower())
            and c.permissions_for(member).send_messages
        ]

    def __init__(self, bot: PathfinderBot):
        self.bot: PathfinderBot = bot
        self.post_dailyfrequenter.start()

    # @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
    @tasks.loop(seconds=30)
    async def post_dailyfrequenter(self):
        for guild_id, settings in self.bot.sm.settings.guilds.items():
            channel = self.bot.get_channel(settings.dailyfrequenter.channel_id)
            if not channel:
                logging.warning(
                    f"Channel {settings.dailyfrequenter.channel_id} not found in guild {guild_id}"
                )
                continue

            if isinstance(channel, TextChannel):
                message = await channel.fetch_message(settings.dailyfrequenter.message_id)

                if not message:
                    logging.warning(
                        f"Message {settings.dailyfrequenter.message_id} not found in guild {guild_id}"
                    )
                    continue

                candidates = pick_paths()
                embed = generate_frequenter_embed(candidates=candidates)
                await message.edit(embed=embed)

    # ---------------------------------------------------------------------------- #
    #                             DAILYFREQUENTER SETUP                            #
    # ---------------------------------------------------------------------------- #
    @dailyfrequenter_commands.command(
        name="setup", description="Setup the automatic daily frequenter"
    )
    @option(
        "channel",
        str,  # int isn't working
        description="Select a channel",
        autocomplete=_channel_autocomplete,
    )
    async def setup_dailyfrequenter(self, ctx: ApplicationContext, channel: str):
        channel_id = int(channel)

        target = self.bot.get_channel(channel_id)
        if not isinstance(target, TextChannel):
            await ctx.respond(
                "Selected channel is not a text channel or cannot be accessed.", ephemeral=True
            )
            return

        candidates = pick_paths()
        embed = generate_frequenter_embed(candidates=candidates)
        message = await target.send(embed=embed)

        gsm = self.bot.sm.get_guild(ctx.guild.id)
        gsm.set_dailyfrequenter(channel_id, message.id)

        await ctx.respond(f"Daily frequenter set up in {target.mention}.", ephemeral=True)

    # ---------------------------------------------------------------------------- #
    #                             DAILYFREQUENTER CLEAR                            #
    # ---------------------------------------------------------------------------- #
    @dailyfrequenter_commands.command(
        name="clear", description="Clear the automatic daily frequenter"
    )
    async def clear_dailyfrequenter(self, ctx: ApplicationContext):
        gsm = self.bot.sm.get_guild(ctx.guild.id)
        gsm.clear_guild()  # we don't have any other guild settings yet - so just remove it

        await ctx.respond("blabla cleared", ephemeral=True)  # TODO


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
def setup(bot):
    bot.add_cog(DailyFrequenterCog(bot))
