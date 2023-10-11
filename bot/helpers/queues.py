import pickle
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
) -> Union[int, bool]:
    """Add or create queue in `group_id` field"""
    kw = [
        {
            "from_user": from_user,
            "is_playing": is_playing,
            "position": position,
            "date": date,
            "file": file,
            "type_of": type_of,
        }
    ]
    values: bytes = pickle.dumps(kw)
    queue: dict = r.hgetall("queues")
    if group_id in str(queue):
        giq: list = pickle.loads(queue[group_id])
        print(giq)
        giq.append(values)
        hset = r.hset("queues", group_id, pickle.dumps(giq))
        if hset == 0:
            return position
        return False
    print(kw)
    hset = r.hset("queues", group_id, values)
    if hset == 1:
        return position
    return False


def next_in_queue(group_id: str) -> Union[Tuple, None]:
    """Get next media in queue"""
    queue: dict = r.hgetall("queues")
    values: list = pickle.loads(queue[group_id])
    if group_id not in str(queue):
        return None
    for i in range(len(values)):
        if values[i].get("is_playing"):
            _next = values[i + 1]
            ot = (
                _next["from_user"],
                _next["is_playing"],
                _next["position"],
                _next["date"],
                _next["file"],
                _next["type_of"],
            )
            return ot
    return None


def previous_in_queue(group_id: str) -> Union[Tuple, None]:
    """Get previous media in queue"""
    queue: dict = r.hgetall("queues")
    values: list = pickle.loads(queue[group_id])
    if group_id not in str(queue):
        return None
    for i in range(len(values)):
        if values[i].get("is_playing"):
            _previous = values[i - 1]
            ot = (
                _previous["from_user"],
                _previous["is_playing"],
                _previous["position"],
                _previous["date"],
                _previous["file"],
                _previous["type_of"],
            )
            return ot
    return None


def remove_queue(group_id: str) -> None:
    """Remove `group_id` from queue"""
    r.hdel("queues", group_id)


def get_queues() -> Union[Dict, None]:
    queues = r.hgetall("queues")
    return queues


def get_current_position_in_queue(group_id: str) -> Union[int, None]:
    """Get the current position of the media that is playing"""
    queue: dict = r.hgetall("queues")
    if group_id not in str(queue):
        return None
    values: dict = pickle.loads(queue[group_id])
    for i in range(len(values)):
        if values[i].get("is_playing"):
            return values[i]["position"]
    return None


def get_last_position_in_queue(group_id: str) -> Union[int, None]:
    """Get the last position of the media that will be played in the queue"""
    queue: dict = r.hgetall("queues")
    if group_id not in str(queue):
        return None
    value: dict = pickle.loads(queue[group_id])[-1]
    print(value)
    return value["position"]


def update_is_played_in_queue(group_id: str, action: str) -> Union[bool, None]:
    """Update `is_playing` status in queue"""
    queue: dict = r.hgetall("queues")
    if group_id not in str(queue):
        return None
    values: list = pickle.loads(queue[group_id])
    for i in range(len(values)):
        if values[i].get("is_playing"):
            if action == "previous":
                values[i]["is_playing"] = False
                values[i - 1]["is_playing"] = True
                return r.hset("queues", group_id, pickle.dumps(values))
            if action == "next":
                values[i]["is_playing"] = False
                values[i + 1]["is_playing"] = True
                return r.hset("queues", group_id, pickle.dumps(values))
    return True
