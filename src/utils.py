import logging
import os
from logging.handlers import RotatingFileHandler
from os import path

from data.schemas import Environment


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    file_handler = RotatingFileHandler(
        path.join(path.dirname(path.realpath(__file__)), "../app.log"),
        maxBytes=10_000_000,  # 10 MB
        backupCount=1,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.getLogger("discord.gateway").setLevel(logging.WARNING)
    logging.getLogger("discord.client").setLevel(logging.WARNING)
    logging.getLogger("discord.http").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("discord.voice").setLevel(logging.WARNING)

    # say hello
    logging.info("\n" + "=" * 80 + "\n" + " " * 32 + "BOT STARTED" + "\n" + "=" * 80)


def setup_env() -> Environment:
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("TOKEN") or ""
    APP_ID = int(os.getenv("APP_ID") or 0)
    DEBUG_GUILD_ID = os.getenv("DEBUG_GUILD_ID")

    if not (TOKEN and APP_ID):
        raise SystemExit("Missing environment variables.")

    return Environment(
        TOKEN=TOKEN,
        APP_ID=APP_ID,
        DEBUG_GUILD_ID=int(DEBUG_GUILD_ID) if DEBUG_GUILD_ID else None,
    )
