import json
import logging
import threading
from dataclasses import asdict
from pathlib import Path

from dacite import from_dict

from data.schemas import Settings


class SettingsManager:
    def __init__(self):
        self.filename = "settings.json"
        self.path = Path(__file__).parents[2] / self.filename
        self.settings: Settings = self._load_or_create()
        self._save_timer: threading.Timer | None = None

    def get_user(self, user_id: int):
        from storage.user_manager import UserSettingsManager

        return UserSettingsManager(self, user_id)

    def get_guild(self, guild_id: int):
        from storage.guild_manager import GuildSettingsManager

        return GuildSettingsManager(self, guild_id)

    def get_guilds(self):
        return [self.get_guild(int(gid)) for gid in self.settings.guilds.keys()]

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
