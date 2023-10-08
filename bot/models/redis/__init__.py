from bot import r
from typing import Tuple, Union

# ------------------------------------------------------------------------


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
    for i, v in range(len(value)):
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
    for i, v in range(len(value)):
        if value[i].get("is_playing"):
            next = value[i - 1]
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


def remove_queue(group_id: str) -> None:
    r.hdel("queues", group_id)


def get_last_queue_position(group_id: str) -> Union[int, None]:
    queue = r.hgetall("queues")
    if group_id not in queue:
        return None
    value = list(queue.values())[-1]
    return value["position"]


# ------------------------------------------------------------------------
