import json
import logging
import threading
from dataclasses import asdict
from pathlib import Path

from dacite import from_dict

from models import Blacklist, Dungeon, GuildSettings, PathID, Settings, UserSettings


class SettingsManager:
    def __init__(self):
        self.filename = "settings.json"
        self.path = Path(__file__).parents[1] / self.filename
        self.settings: Settings = self._load_or_create()
        self._save_timer: threading.Timer | None = None

    def get_user(self, user_id: int):
        return UserSettingsManager(self, user_id)

    def get_guild(self, guild_id: int):
        return GuildSettingsManager(self, guild_id)

    # ---------------------------------------------------------------------------- #
    #                                 SETTINGS.JSON                                #
    # ---------------------------------------------------------------------------- #

    def _load_or_create(self) -> Settings:
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            logging.info(f"Loaded settings from {self.path}")
            return from_dict(Settings, data)
        except FileNotFoundError:
            logging.warning(f"No settings file found at {self.path}, creating new one")
            settings = Settings()
            self.settings = settings
            self.save()
            return settings
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted settings file: {e}") from e

    def _debounced_save(self):
        if self._save_timer:
            self._save_timer.cancel()
        self._save_timer = threading.Timer(2, self.save)
        self._save_timer.start()

    def save(self) -> None:
        if not self.settings:
            return

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(asdict(self.settings), f, indent=4, ensure_ascii=False)
            logging.info(f"Settings saved to {self.path}")
        except OSError as err:
            logging.exception(f"I/O error while saving settings: {err}")

    def mark_dirty(self):
        self._debounced_save()


class UserSettingsManager:
    def __init__(self, sm: SettingsManager, user_id: int):
        self.sm = sm
        self.user_id = str(user_id)

        self.sm.settings.users.setdefault(self.user_id, UserSettings())

    def get_blacklist(self) -> Blacklist:
        return self.sm.settings.users.setdefault(self.user_id, UserSettings()).blacklist

    def blacklist_add(self, dungeon: Dungeon, path_id: PathID | None = None):
        user_settings = self.sm.settings.users[self.user_id]

        if dungeon.id not in user_settings.blacklist:
            user_settings.blacklist[dungeon.id] = []

        if path_id is not None:
            if path_id not in user_settings.blacklist[dungeon.id]:
                user_settings.blacklist[dungeon.id].append(path_id)
                user_settings.blacklist[dungeon.id].sort()
        else:
            user_settings.blacklist[dungeon.id] = [p.id for p in dungeon.paths if not p.hidden]

        self.sm.mark_dirty()

    def blacklist_remove(self, dungeon: Dungeon, path_id: PathID | None = None):
        user_settings = self.sm.settings.users[self.user_id]

        if dungeon.id in user_settings.blacklist:
            if path_id is not None:
                if path_id in user_settings.blacklist[dungeon.id]:
                    user_settings.blacklist[dungeon.id].remove(path_id)
                if len(user_settings.blacklist[dungeon.id]) == 0:
                    del user_settings.blacklist[dungeon.id]
            else:
                del user_settings.blacklist[dungeon.id]

        self.sm.mark_dirty()

    def blacklist_clear(self):
        if self.user_id in self.sm.settings.users:
            self.sm.settings.users[self.user_id].blacklist.clear()
            self.sm.mark_dirty()

    def clear_user(self):
        if self.user_id in self.sm.settings.users:
            del self.sm.settings.users[self.user_id]
            self.sm.mark_dirty()


class GuildSettingsManager:
    def __init__(self, sm: SettingsManager, guild_id: int):
        self.sm = sm
        self.guild_id = str(guild_id)

        self.sm.settings.guilds.setdefault(self.guild_id, GuildSettings())

    def set_dailyfrequenter(self, channel_id: int, message_id: int):
        g = self.sm.settings.guilds[self.guild_id]
        g.dailyfrequenter.channel_id = channel_id
        g.dailyfrequenter.message_id = message_id
        self.sm.mark_dirty()

    def unset_dailyfrequenter(self):
        g = self.sm.settings.guilds[self.guild_id]
        g.dailyfrequenter = GuildSettings().dailyfrequenter
        self.sm.mark_dirty()

    def clear_guild(self):
        if self.guild_id in self.sm.settings.guilds:
            del self.sm.settings.guilds[self.guild_id]
            self.sm.mark_dirty()
