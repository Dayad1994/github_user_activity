"""Fetch data module."""

import requests

from gua.typing import GroupedEvents


def fetch_events(url: str) -> GroupedEvents:
    return requests.get(url).json()
