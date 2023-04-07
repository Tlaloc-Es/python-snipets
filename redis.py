import time
import json


def zadd(redis, key, data):
    """[summary]

    Add data into a redis zset

    Args:
        redis ([type]): Redis connection
        key ([type]): Zset key
        data ([type]): Data as a python dict
    """
    ts = time.time()
    redis.zadd(key, {json.dumps(data): ts})


def zpopmindict(redis, key, total):
    return json.loads(redis.zpopmin(key, total)[0][0].decode('utf-8'))
