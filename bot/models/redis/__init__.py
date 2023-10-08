from bot import r
from typing import Tuple, Union

# ------------------------------------------------------------------------


def add_to_queue(group_id: str, from_user: str,position:int, date: str, file:str, type:str) -> bool:
    """Add or create queue from group_id"""
    values = {
        "from_user": from_user,
        "position": position,
        "date": date,
        "file": file,
        "type": type,
        
    }
    hset = r.hset("queues", group_id, values)
    return hset


def next_in_queue(group_id: str) -> Union[Tuple, None]:
    queue = r.hgetall("queues")
    value = queue[group_id]
    if not value:
        return None
    values = (value["from_user"], value["position"], value["date"], value["file"], value["type"])
    return values


def remove_queue(group_id: str):
    queue = r.hgetall("queues")
    hdel = r.hdel("queues", group_id)
    return hdel

def get_queue_position(group_id: str) -> Union[int, None]:
    queue = r.hgetall("queues")
    if not queue:
        return None
    value = list(queue.values())[-1]
    return value["position"]

# ------------------------------------------------------------------------