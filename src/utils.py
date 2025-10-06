import logging
import os
from os import path
from pathlib import Path

from data.schemas import Environment


def setup_logging():
    log_file_path = path.join(path.dirname(path.realpath(__file__)), "../app.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def setup_env() -> Environment:
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("TOKEN") or ""
    app_id = int(os.getenv("APP_ID") or 0)
    guild_id = os.getenv("GUILD_ID")

    if not (token and app_id):
        raise SystemExit("Missing environment variables.")

    return Environment(
        token=token,
        app_id=app_id,
        guild_id=int(guild_id) if guild_id else None,
        root=Path(__file__).resolve().parents[1],
    )
