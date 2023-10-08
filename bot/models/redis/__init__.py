from bot import r
from typing import Tuple, Union


def add_to_queue(
    group_id: str,
    from_user: str,
    is_playing: bool,
    date: str,
    file: str,
    type: str,
    position=1,
) -> bool:
    """Add or create queue in `group_id` field"""
    values = [
        {
            "from_user": from_user,
            "is_playing": is_playing,
            "position": position,
            "date": date,
            "file": file,
            "type": type,
        }
    ]
    queue = r.hgetall("queues")
    if group_id in queue:
        queue[group_id].append(values)
        hset = r.hset("queues", group_id, queue[group_id])
        if hset == 0:
            return True
        return False
    hset = r.hset("queues", group_id, values)
    if hset == 1:
        return True
    return False


def next_in_queue(group_id: str) -> Union[Tuple, None]:
    queue = r.hgetall("queues")
    value = queue[group_id]
    if group_id not in queue:
        return None
    for i in range(len(value)):
        if value[i].get("is_playing"):
            next = value[i + 1]
            values = (
                next["from_user"],
                next["is_playing"],
                next["position"],
                next["date"],
                next["file"],
                next["type"],
            )
            return values
    return None


def previous_in_queue(group_id: str) -> Union[Tuple, None]:
    queue = r.hgetall("queues")
    value = queue[group_id]
    if group_id not in queue:
        return None
    for i in range(len(value)):
        if value[i].get("is_playing"):
            previous = value[i - 1]
            values = (
                previous["from_user"],
                previous["is_playing"],
                previous["position"],
                previous["date"],
                previous["file"],
                previous["type"],
            )
            return values
    return None


def remove_queue(group_id: str) -> None:
    r.hdel("queues", group_id)


def get_current_position_in_queue(group_id: str) -> Union[int, None]:
    queue = r.hgetall("queues")
    if group_id not in queue:
        return None
    values = queue[group_id].values()[-1]
    for i in range(len(values)):
        if values[i].get("is_playing"):
            return values[i]["position"]
    return None


def get_last_position_in_queue(group_id: str) -> Union[int, None]:
    queue = r.hgetall("queues")
    if group_id not in queue:
        return None
    value = queue[group_id].values()[-1]
    return value["position"]


def update_is_played_in_queue(action: str) -> None:
    queue = r.hgetall("queues")
    values = queue[group_id]
    if group_id not in queue:
        return None
    for i in range(len(values)):
        if values[i].get("is_playing"):
            if action == "previous":
                values[i]["is_playing"] = False
                values[i - 1]["is_playing"] = True
                return r.hset("queues", group_id, values)
            elif action == "next":
                values[i]["is_playing"] = False
                values[i + 1]["is_playing"] = True
                return r.hset("queues", group_id, values)
    return None
