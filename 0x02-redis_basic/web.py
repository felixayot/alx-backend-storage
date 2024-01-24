#!/usr/bin/env python3
"""Module for Redis page access and retrieval implementations."""
import requests
from redis import Redis
from functools import wraps
from typing import Callable

redis = Redis()


def count_requests(method: Callable) -> Callable:
    """
     Track the number of times a particular URL was accessed in the key.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper for decorator.
        """
        redis.incr(f"count:{url}")
        cached_html = redis.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a  URL.
    """
    req = requests.get(url)
    return req.text
