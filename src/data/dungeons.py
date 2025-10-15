from data.emojis import BotEmojis
from data.schemas import Dungeon, DungeonPath

DUNGEONS: list[Dungeon] = [
    Dungeon(
        id="AC",
        name="Ascalonian Catacombs",
        emoji=BotEmojis.AC,
        paths=[
            DungeonPath(0, "Story", 30, "Night", True),
            DungeonPath(1, "Path 1 — `Hodgins`", 35, "Night", False),
            DungeonPath(2, "Path 2 — `Detha`", 35, "Night", False),
            DungeonPath(3, "Path 3 — `Tzark`", 35, "Night", False),
        ],
    ),
    Dungeon(
        id="CM",
        name="Caudecus's Manor",
        emoji=BotEmojis.CM,
        paths=[
            DungeonPath(0, "Story", 40, "Day", True),
            DungeonPath(1, "Path 1 — `Asura`", 45, "Day", False),
            DungeonPath(2, "Path 2 — `Seraph`", 45, "Day", False),
            DungeonPath(3, "Path 3 — `Butler`", 45, "Day", False),
        ],
    ),
    Dungeon(
        id="TA",
        name="Twilight Arbor",
        emoji=BotEmojis.TA,
        paths=[
            DungeonPath(0, "Story", 50, "Night", True),
            DungeonPath(1, "Forward — `Vevina`", 55, "Night", False),
            DungeonPath(2, "Up — `Leurent`", 55, "Night", False),
            DungeonPath(3, "Aetherpath", 80, "Night", False),
        ],
    ),
    Dungeon(
        id="SE",
        name="Sorrow's Embrace",
        emoji=BotEmojis.SE,
        paths=[
            DungeonPath(0, "Story", 60, "Night", True),
            DungeonPath(1, "Path 1 — `Fergg`", 65, "Night", False),
            DungeonPath(2, "Path 2 — `Rasolov`", 65, "Night", False),
            DungeonPath(3, "Path 3 — `Koptev`", 65, "Night", False),
        ],
    ),
    Dungeon(
        id="CoF",
        name="Citadel of Flame",
        emoji=BotEmojis.COF,
        paths=[
            DungeonPath(0, "Story", 70, "Night", True),
            DungeonPath(1, "Path 1 — `Ferrah`", 75, "Night", False),
            DungeonPath(2, "Path 2 — `Magg`", 75, "Night", False),
            DungeonPath(3, "Path 3 — `Rhiannon`", 75, "Night", False),
        ],
    ),
    Dungeon(
        id="HotW",
        name="Honor of the Waves",
        emoji=BotEmojis.HOTW,
        paths=[
            DungeonPath(0, "Story", 76, "Day", True),
            DungeonPath(1, "Path 1 — `Butcher`", 80, "Day", False),
            DungeonPath(2, "Path 2 — `Plunderer`", 80, "Day", False),
            DungeonPath(3, "Path 3 — `Zealot`", 80, "Day", False),
        ],
    ),
    Dungeon(
        id="CoE",
        name="Crucible of Eternity",
        emoji=BotEmojis.COE,
        paths=[
            DungeonPath(0, "Story", 78, "Day", True),
            DungeonPath(1, "Path 1 — `Submarine`", 80, "Night", False),
            DungeonPath(2, "Path 2 — `Teleporter`", 80, "Night", False),
            DungeonPath(3, "Path 3 — `Front Door`", 80, "Night", False),
        ],
    ),
    Dungeon(
        id="Arah",
        name="The Ruined City of Arah",
        emoji=BotEmojis.ARAH,
        paths=[
            # Arah Story is not included because it cannot be replayed
            DungeonPath(1, "Path 1 — `Jotun`", 80, "Day", False),
            DungeonPath(2, "Path 2 — `Mursaat`", 80, "Day", False),
            DungeonPath(3, "Path 3 — `Forgotten`", 80, "Day", False),
            DungeonPath(4, "Path 4 — `Seer`", 80, "Day", False),
        ],
    ),
]
