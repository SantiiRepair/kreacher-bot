from bot import r


# ------------------------------------------------------------------------
def add_to_queue(group_id, from_user, date):
    values = {"from_user": from_user, "date": date}
    hset = r.hset("queues", group_id, values)
    return hset


def next_in_queue():
    queue = r.hgetall("queues").popitem()
    group_id = queue[0]
    value = queue[1]
    hdel = r.hdel("queues", group_id)
    return hdel


# ------------------------------------------------------------------------
