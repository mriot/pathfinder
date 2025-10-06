from data.schemas import Blacklist, Dungeon, PathID, UserSettings
from storage.settings_manager import SettingsManager


class UserSettingsManager:
    def __init__(self, sm: SettingsManager, user_id: int):
        self.sm = sm
        self.user_id = str(user_id)

        self.sm.settings.users.setdefault(self.user_id, UserSettings())

    def get_blacklist(self) -> Blacklist:
        return self.sm.settings.users[self.user_id].blacklist

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
