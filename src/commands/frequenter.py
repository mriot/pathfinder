from discord import ApplicationContext
from discord.commands import option
from discord.ext import commands

from dungeons import DUNGEONS
from main import PathfinderBot, generate_frequenter_embed, pick_paths


class FrequenterCog(commands.Cog):
    # @staticmethod
    # def _tod_emoji(value: str) -> str:
    #     return "<:night_sigil:1423998252705120390>" if value.lower() == "night" else ""

    # @staticmethod
    # def generate_frequenter_embed(candidates: List[Candidate]):
    #     dungeon_sections = []
    #     sorted_candidates = sorted(candidates, key=lambda x: x.dungeon_id)  # makes grouping easier
    #     for dungeon_id, group in itertools.groupby(sorted_candidates, key=lambda x: (x.dungeon_id)):
    #         dungeon = next(d for d in DUNGEONS if d.id == dungeon_id)
    #         paths = []

    #         for candidate in sorted(group, key=lambda x: x.path_id):
    #             path = next(p for p in dungeon.paths if p.id == candidate.path_id)
    #             paths.append(f"{path.name} {Frequenter._tod_emoji(path.time_of_day)}")

    #         dungeon_sections.append(
    #             f"### {dungeon.emoji} {dungeon.name}" + "\n - ".join(["", *paths])
    #         )

    #     random.shuffle(dungeon_sections)
    #     embed = discord.Embed()
    #     embed.description = "\n".join(dungeon_sections)
    #     embed.set_footer(text=f"Generated {len(candidates)} paths for you. Enjoy!")

    #     return embed

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
        candidates = pick_paths(
            DUNGEONS,
            blacklist=self.bot.sm.user_blacklist(ctx.author.id),
            path_count=path_count,
            no_story=no_story,
            time_of_day=time_of_day,
            ignore_filters=ignore_filters,
        )

        embed = generate_frequenter_embed(candidates=candidates)
        await ctx.respond(embed=embed)

    # ---------------- frequenter commands below are just aliases ---------------- #

    # ---------------------------------------------------------------------------- #
    #                               NIGHT FREQUENTER                               #
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
    #                                DAY FREQUENTER                                #
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
    #                               CHAOS FREQUENTER                               #
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
