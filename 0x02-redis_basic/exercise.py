#!/usr/bin/env python3
"""Cache class definition."""
from redis import Redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Increments the count for a key
    every time the method is called.
    Returns the value
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            Wrapper function.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A Decorator for storing the history of inputs and outputs
    for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper for decorator functionality
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls of a particular function.
    """
    name = method.__qualname__
    cache = Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """
    Represents a cache.
    """
    def __init__(self):
        """
        Initializes a cache instance and gets rid of it after.
        """
        self._redis = Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key for input data.
        Takes a data argument and returns a string.
        """
        rand_key = str(uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves data from the Redis server.
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from the cache.
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer from the cache.
        """
        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0
        return data
