import random
from typing import List

from data.dungeons import DUNGEONS
from data.schemas import Blacklist, Candidate, Dungeon


def pick_paths(
    dungeons: List[Dungeon] = DUNGEONS,
    blacklist: Blacklist = {},
    path_count: int = 8,
    no_story: bool = False,
    time_of_day: str | None = None,
    ignore_filters: bool = False,
) -> List[Candidate]:
    if path_count <= 0:
        return []

    candidates: List[Candidate] = []

    for dungeon in dungeons:
        excluded = blacklist.get(dungeon.id)

        # TODO might be wrong?
        if not ignore_filters and excluded == []:
            continue  # entire dungeon excluded

        for path in dungeon.paths:
            if path.hidden:
                continue
            if not ignore_filters:
                if isinstance(excluded, list) and path.id in excluded:
                    continue
                if no_story and path.story:
                    continue
                if time_of_day and path.time_of_day.lower() != time_of_day.lower():
                    continue

            candidates.append(Candidate(dungeon.id, path.id))

    return random.sample(candidates, min(path_count, len(candidates)))
