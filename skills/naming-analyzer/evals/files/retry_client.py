import time

import requests

MAX = 5
DEFAULT_TIMEOUT = 30  # passed straight to requests, which takes seconds


class user_profile:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines


def calc_ttl(arr):
    t = 0
    for x in arr:
        t += x.amount
    return t


def fetch_profile(url):
    for attempt in range(MAX):
        try:
            return requests.get(url, timeout=DEFAULT_TIMEOUT).json()
        except requests.RequestException:
            time.sleep(2 ** attempt)
    raise RuntimeError("profile service unavailable")
