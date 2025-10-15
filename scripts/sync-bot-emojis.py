import asyncio
import json
import os
from pathlib import Path

import discord
from dotenv import load_dotenv

# This script syncs the bot's emojis from Discord and saves them to a JSON file.
# Manually run this script whenever you add/remove emojis to/from your bot.


async def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN") or ""
    APP_ID = int(os.getenv("APP_ID") or 0)

    if not (TOKEN and APP_ID):
        raise SystemExit("Missing environment variables.")

    intents = discord.Intents.none()
    client = discord.Client(intents=intents, application_id=APP_ID)
    await client.login(TOKEN)

    route = discord.http.Route("GET", f"/applications/{client.application_id}/emojis")
    data = await client.http.request(route)
    await client.close()

    # Note: names are normalized to lowercase to avoid issues with case sensitivity
    mapping = {e["name"].lower(): e["id"] for e in data["items"]}

    out_file = Path(__file__).parents[1] / "emoji_data.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)

    print(f"Saved {len(mapping)} emojis to {out_file}")


if __name__ == "__main__":
    asyncio.run(main())
