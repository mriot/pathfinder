import logging

from discord import ApplicationContext, OptionChoice, SlashCommandGroup, option
from discord.ext import commands, tasks

from main import PathfinderBot, generate_frequenter_embed, pick_paths


class DailyFrequenterCog(commands.Cog):
    dailyfrequenter_commands = SlashCommandGroup(
        "dailyfrequenter", "Manage the automatic daily frequenter"
    )

    def _channel_id_autocomplete(self, ctx: ApplicationContext, query: str):
        return [
            OptionChoice(name=c.name, value=str(c.id))
            for c in ctx.guild.channels
            if query.lower() in c.name.lower()
        ]

    def __init__(self, bot: PathfinderBot):
        self.bot: PathfinderBot = bot
        self.post_dailyfrequenter.start()

    @tasks.loop(seconds=10)
    async def post_dailyfrequenter(self):
        for guild_id, settings in self.bot.sm.settings.guilds.items():
            channel = self.bot.get_channel(settings.dailyfrequenter.channel_id)
            if not channel:
                logging.warning(
                    f"Channel {settings.dailyfrequenter.channel_id} not found in guild {guild_id}"
                )
                continue

            message = self.bot.get_message(settings.dailyfrequenter.message_id)
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
        autocomplete=lambda ctx: [
            OptionChoice(name=c.name, value=str(c.id))
            for c in ctx.interaction.guild.channels
            if c.name.lower().startswith(ctx.value.lower())
        ],
    )
    async def setup_dailyfrequenter(self, ctx: ApplicationContext, channel: str):
        guild_settings = self.bot.sm.guild_settings(ctx.guild.id)
        guild_settings.dailyfrequenter.channel_id = int(channel)

        await ctx.respond("blabla set up", ephemeral=True)

        candidates = pick_paths()
        embed = generate_frequenter_embed(candidates=candidates)

        message = await ctx.respond(embed=embed)
        guild_settings.dailyfrequenter.message_id = message.id

        # await ctx.interaction.edit_original_response(content="Updated text")

        self.bot.sm.mark_dirty()
        # embed = discord.Embed(title="Daily frequenter setup")
        # embed.add_field(name="Channel", value=channel)
        # await ctx.respond(embed=embed, ephemeral=True)


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
def setup(bot):
    bot.add_cog(DailyFrequenterCog(bot))
