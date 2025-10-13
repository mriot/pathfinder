from data.schemas import DailyFrequenter, GuildSettings
from storage.settings_manager import SettingsManager


class GuildSettingsManager:
    def __init__(self, sm: SettingsManager, guild_id: int):
        self.sm = sm
        self.guild_id = guild_id

        self.sm.settings.guilds.setdefault(self.guild_id, GuildSettings())

    def get_dailyfrequenter(self) -> DailyFrequenter:
        return self.sm.settings.guilds[self.guild_id].dailyfrequenter

    def set_dailyfrequenter(self, channel_id: int, message_id: int):
        g = self.sm.settings.guilds[self.guild_id]
        g.dailyfrequenter.channel_id = channel_id
        g.dailyfrequenter.message_id = message_id
        self.sm.mark_dirty()

    def unset_dailyfrequenter(self):
        # NOTE: currently we don't have any other guild related settings, so we just clear everything
        self.clear_guild()

        # g = self.sm.settings.guilds[self.guild_id]
        # g.dailyfrequenter = GuildSettings().dailyfrequenter
        # self.sm.mark_dirty()

    def clear_guild(self):
        if self.guild_id in self.sm.settings.guilds:
            del self.sm.settings.guilds[self.guild_id]
            self.sm.mark_dirty()
