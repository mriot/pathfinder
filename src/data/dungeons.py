from data.schemas import Dungeon, DungeonPath

DUNGEONS: list[Dungeon] = [
    Dungeon(
        id="AC",
        name="Ascalonian Catacombs",
        emoji="<:ac:1423759741103898674>",
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
        emoji="<:cm:1423759758447349894>",
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
        emoji="<:ta:1423759793637822464>",
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
        emoji="<:se:1423759851376611338>",
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
        emoji="<:cof:1423759875741319289>",
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
        emoji="<:hotw:1423759894888059052>",
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
        emoji="<:coe:1423759921035345993>",
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
        emoji="<:arah:1423759936239829083>",
        paths=[
            DungeonPath(0, "Story", 80, "Day", True, hidden=True),
            DungeonPath(1, "Path 1 — `Jotun`", 80, "Day", False),
            DungeonPath(2, "Path 2 — `Mursaat`", 80, "Day", False),
            DungeonPath(3, "Path 3 — `Forgotten`", 80, "Day", False),
            DungeonPath(4, "Path 4 — `Seer`", 80, "Day", False),
        ],
    ),
]
