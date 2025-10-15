import asyncio
import datetime
import logging
import re

import discord
from discord import ApplicationContext
from discord.commands import option
from discord.ext import commands

from core.bot import PathfinderBot
from data.emojis import BotEmojis


class LfgCog(commands.Cog):
    def __init__(self, bot: PathfinderBot):
        self.bot: PathfinderBot = bot

    @staticmethod
    def parse_time(raw: str) -> int:
        raw = raw.strip().lower()
        now = datetime.datetime.now().astimezone()
        time_formats = [
            "%H:%M",  # 15:00
            "%H.%M",  # 15.00
            "%H",  # 15
            "%I%p",  # 3pm
            "%I:%M%p",  # 3:30pm
            "%I.%M%p",  # 3.30pm
        ]

        # absolute time
        for fmt in time_formats:
            try:
                parsed_time = datetime.datetime.strptime(raw, fmt)

                target_time = now.replace(
                    hour=parsed_time.hour,
                    minute=parsed_time.minute,
                    second=0,
                    microsecond=0,
                )

                if target_time < now:
                    target_time += datetime.timedelta(days=1)

                return int(target_time.timestamp())
            except ValueError:
                continue

        # relative time
        if match := re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?", raw):
            hours, minutes = map(int, match.groups(default="0"))
            if hours > 24 or minutes > 999:
                raise ValueError(raw)
            target_time = now + datetime.timedelta(hours=int(hours), minutes=int(minutes))
            return int(target_time.timestamp())

        logging.info(f"Failed to parse time: {raw}")
        raise ValueError(raw)

    # ---------------------------------------------------------------------------- #
    #                               LOOKING FOR GROUP                              #
    # ---------------------------------------------------------------------------- #
    @commands.slash_command(name="lfg", description="Looking for group")
    @option("ping_role", discord.Role, description="Role to ping")
    @option("time", str, description="HH:MM (e.g. 15:00) or relative like 1h30m")
    @option("lfg_message", str, description="Optional LFG message", required=False)
    async def lfg(
        self,
        ctx: ApplicationContext,
        ping_role: discord.Role,
        time: str,
        lfg_message: str = "",
    ):
        message_parts = [f"{BotEmojis.LFG} LFG"]
        message_parts.append(ping_role.mention)

        try:
            parsed_time = self.parse_time(time)
            event_time = f"<t:{parsed_time}:R> @ <t:{parsed_time}:t>"
            message_parts.append(event_time)
        except ValueError as e:
            await ctx.respond(
                f"Sorry, I could not parse `{e}` as time.\n"
                "Try `HH:MM` (e.g. `15:00`) or relative values like `1h30m`.",
                ephemeral=True,
            )
            return

        if lfg_message:
            message_parts.append(f"— {lfg_message}")

        message = " ".join(message_parts)

        view = ParticipationView(message)
        view.members.add(ctx.author.id)
        await ctx.respond(view.render_text(), view=view)


# ---------------------------------------------------------------------------- #
#                              PARTICIPATION VIEW                              #
# ---------------------------------------------------------------------------- #


class ParticipationView(discord.ui.View):
    def __init__(self, message_text: str):
        super().__init__()
        self.message_text = message_text
        self.members: set[int] = set()
        self._message_lifetime = 15
        self._delete_task: asyncio.Task | None = None

    async def _delete_message_task(self):
        await asyncio.sleep(self._message_lifetime)
        # note: self.message is only set after user interaction
        if self.message and not self.members:
            try:
                await self.message.delete()
            except discord.NotFound:
                pass

    def render_text(self) -> str:
        names = [f"<@{m}>" for m in self.members]
        removal_time = int(datetime.datetime.now().timestamp() + self._message_lifetime + 1)

        return self.message_text + (
            f"\n### Players ({len(names)}): " + (", ".join(names))
            if names
            else "\n### No one yet :neutral_face:\n"
            + f"*LFG will be removed <t:{removal_time}:R> if no one signs up*"
        )

    @discord.ui.button(
        emoji=BotEmojis.Yes, label="Sign me up!", style=discord.ButtonStyle.secondary
    )
    async def joinleave(self, button, interaction: discord.Interaction):
        if not (user := interaction.user):
            return

        self.members.symmetric_difference_update({user.id})  # fancy toggle

        await interaction.response.edit_message(content=self.render_text(), view=self)

        # delete message after a while if no members remain
        if not self.members:
            if self._delete_task:
                self._delete_task.cancel()
            self._delete_task = asyncio.create_task(self._delete_message_task())


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
def setup(bot):
    bot.add_cog(LfgCog(bot))
