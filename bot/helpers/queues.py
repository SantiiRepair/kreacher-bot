from bot import r
from typing import Dict, Tuple, Union


def add_or_create_queue(
    group_id: str,
    from_user: str,
    date: str,
    file: str,
    type_of: str,
    is_playing=False,
    position=0,
) -> Union[Tuple, bool]:
    """Add or create queue in `group_id` field"""
    values = [
        {
            "from_user": from_user,
            "is_playing": is_playing,
            "position": position,
            "date": date,
            "file": file,
            "type_of": type_of,
        }
    ]
    queue: dict = r.hgetall("queues")
    if group_id in queue:
        queue[group_id].append(values)
        hset = r.hset("queues", group_id, queue[group_id])
        if hset == 0:
            return True, position
        return False
    hset = r.hset("queues", group_id, values)
    if hset == 1:
        return True, position
    return False


def next_in_queue(group_id: str) -> Union[Tuple, None]:
    """Get next media in queue"""
    queue: dict = r.hgetall("queues")
    values: list = queue[group_id]
    if group_id not in queue:
        return None
    for i in range(len(values)):
        if values[i].get("is_playing"):
            _next = values[i + 1]
            tdo = (
                _next["from_user"],
                _next["is_playing"],
                _next["position"],
                _next["date"],
                _next["file"],
                _next["type_of"],
            )
            return tdo
    return None


def previous_in_queue(group_id: str) -> Union[Tuple, None]:
    """Get previous media in queue"""
    queue: dict = r.hgetall("queues")
    values: list = queue[group_id]
    if group_id not in queue:
        return None
    for i in range(len(values)):
        if values[i].get("is_playing"):
            _previous = values[i - 1]
            tdo = (
                _previous["from_user"],
                _previous["is_playing"],
                _previous["position"],
                _previous["date"],
                _previous["file"],
                _previous["type_of"],
            )
            return tdo
    return None


def remove_queue(group_id: str) -> None:
    """Remove `group_id` from queue"""
    r.hdel("queues", group_id)


def get_current_position_in_queue(group_id: str) -> Union[int, None]:
    """Get the current position of the media that is playing"""
    queue: dict = r.hgetall("queues")
    if group_id not in queue:
        return None
    values: dict = queue[group_id][-1]
    for i in range(len(values)):
        if values[i].get("is_playing"):
            return values[i]["position"]
    return None


def get_last_position_in_queue(group_id: str) -> Union[int, None]:
    """Get the last position of the media that will be played in the queue"""
    queue: dict = r.hgetall("queues")
    if group_id not in queue:
        return None
    value: dict = queue[group_id][-1]
    return value["position"]


def get_queues() -> Union[Dict, None]:
    return r.hgetall("queues")


def update_is_played_in_queue(group_id: str, action: str) -> None:
    """Update `is_playing` status in queue"""
    queue: dict = r.hgetall("queues")
    values: list = queue[group_id]
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
