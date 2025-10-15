import json
import logging
from pathlib import Path


class BotEmojis:
    """
    Holds the bot's custom emojis loaded from a JSON file.
    Access emojis as class attributes, e.g. `BotEmojis.LFG`.
    """

    # Note: only emojis defined here will be loaded from the JSON file
    # The names must match the names of the emojis in Discord (case-insensitive)
    LFG: str
    TICK: str
    CROSS: str
    NIGHT_SIGIL: str
    DUNGEON: str
    AC: str
    CM: str
    TA: str
    SE: str
    COF: str
    HOTW: str
    COE: str
    ARAH: str

    _emoji_data: dict[str, str] = {}

    @classmethod
    def load(cls, path=Path(__file__).parents[2] / "emoji_data.json"):
        try:
            cls._emoji_data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise SystemExit(f"{path} not found! Make sure to sync emojis first using the script.")
        except json.JSONDecodeError as e:
            raise SystemExit(f"Failed to parse {path}: {e}")

        emoji_count = 0
        for name in cls.__annotations__:
            if name.startswith("_"):
                continue

            if not (id := cls._emoji_data.get(name.lower())):
                raise SystemExit(f"Emoji '{name}' not found in {path}")

            setattr(cls, name, f"<:{name}:{id}>")
            emoji_count += 1

        if len(cls._emoji_data) != emoji_count:
            logging.warning(
                f"Loaded {emoji_count} emojis, but {len(cls._emoji_data)} exist in {path}."
            )
        else:
            logging.info(f"Loaded {emoji_count} emojis")
