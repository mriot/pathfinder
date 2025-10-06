from discord import ApplicationContext
from discord.commands import option
from discord.ext import commands

from core.bot import PathfinderBot
from core.frequenter_embed import generate_frequenter_embed
from core.path_picker import pick_paths
from data.dungeons import DUNGEONS


class FrequenterCog(commands.Cog):
    def __init__(self, bot: PathfinderBot):
        self.bot: PathfinderBot = bot

    # ---------------------------------------------------------------------------- #
    #                               FREQUENTER - MAIN                              #
    # ---------------------------------------------------------------------------- #
    @commands.slash_command(name="frequenter", description="Generate a frequenter route")
    @option("path_count", int, description="Number of paths to generate")
    @option("no_story", bool, description="Exclude story paths?")
    @option("time_of_day", str, description="Filter by time of day", choices=["day", "night"])
    @option("ignore_filters", bool, description="Ignores blacklist and filters")
    async def frequenter(
        self,
        ctx: ApplicationContext,
        path_count: int = 8,
        no_story: bool = False,
        time_of_day: str | None = None,
        ignore_filters: bool = False,
    ):
        if path_count <= 0:
            return await ctx.respond(
                "https://tenor.com/view/rickroll-bailu-gif-13109126276794815880", ephemeral=True
            )

        usm = self.bot.sm.get_user(ctx.author.id)

        candidates = pick_paths(
            DUNGEONS,
            blacklist=usm.get_blacklist(),
            path_count=path_count,
            no_story=no_story,
            time_of_day=time_of_day,
            ignore_filters=ignore_filters,
        )

        embed = generate_frequenter_embed(candidates=candidates)
        await ctx.respond(embed=embed)

    # ---------------------------------------------------------------------------- #
    #                            NIGHT FREQUENTER ALIAS                            #
    # ---------------------------------------------------------------------------- #
    @commands.slash_command(
        name="nightfrequenter", description="Generate a frequenter route with only night time paths"
    )
    @option("paths", int, description="Number of paths to generate")
    @option("no_story", bool, description="Exclude story paths?")
    async def nightfrequenter(
        self, ctx: ApplicationContext, path_count: int = 8, no_story: bool = False
    ):
        await self.frequenter(ctx, path_count, no_story=no_story, time_of_day="night")

    # ---------------------------------------------------------------------------- #
    #                             DAY FREQUENTER ALIAS                             #
    # ---------------------------------------------------------------------------- #
    @commands.slash_command(
        name="dayfrequenter", description="Generate a frequenter route with only day time paths"
    )
    @option("paths", int, description="Number of paths to generate")
    @option("no_story", bool, description="Exclude story paths?")
    async def dayfrequenter(
        self, ctx: ApplicationContext, path_count: int = 8, no_story: bool = False
    ):
        await self.frequenter(ctx, path_count, no_story=no_story, time_of_day="day")

    # ---------------------------------------------------------------------------- #
    #                            CHAOS FREQUENTER ALIAS                            #
    # ---------------------------------------------------------------------------- #
    @commands.slash_command(
        name="chaosfrequenter", description="Generate a random frequenter route"
    )
    @option("paths", int, description="Number of paths to generate")
    async def chaosfrequenter(self, ctx: ApplicationContext, path_count: int = 8):
        await self.frequenter(ctx, path_count, ignore_filters=True)


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
def setup(bot):
    bot.add_cog(FrequenterCog(bot))
