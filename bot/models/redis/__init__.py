from bot import r
from typing import Tuple, Union


# ------------------------------------------------------------------------
def add_to_queue(group_id, from_user, date) -> bool:
    values = {"from_user": from_user, "date": date}
    hset = r.hset("queues", group_id, values)
    return hset


def next_in_queue() -> Union[Tuple, None]:
    queue = r.hgetall("queues").popitem()
    value = queue[1]
    if not value:
        return None
    return value["from_user"], value["date"], value[""]


def remove_queue():
    queue = r.hgetall("queues").popitem()
    group_id = queue[0]
    hdel = r.hdel("queues", group_id)
    return hdel


# ------------------------------------------------------------------------
