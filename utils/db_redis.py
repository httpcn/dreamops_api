#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : httpcn

from redis import ConnectionPool, StrictRedis, ConnectionError

from config import Settings as S


class RedisDB:
    def __init__(self, pipeline=False):
        self.pipeline = pipeline
        self.db = None

    def __enter__(self):
        pool = ConnectionPool(
            host=S.REDIS_HOST,
            port=S.REDIS_PORT,
            decode_responses=True
        )
        self.db = StrictRedis(connection_pool=pool, max_connections=S.REDIS_MAXCONN)

        if self.pipeline:
            return self.db.pipeline()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == ConnectionError or exc_type is not None:
            print('Error:', exc_val)
            self.db.close()
            return True


def rdb(pipeline=False):
    with RedisDB(pipeline) as _rdb:
        pass


if __name__ == '__main__':
    with RedisDB() as rdb:
        rdb.setnx(name=S.ver, value='0.0.1')
        print(rdb.get(name=S.ver))

    # with RedisDB(pipeline=True) as rdb_pipe:
    #     for i in range(10):
    #         rdb_pipe.set(f'test-{i}', i)
    #     rdb_pipe.execute()
