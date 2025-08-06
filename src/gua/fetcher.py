"""Fetch data module."""

import requests

from gua.event_types import GroupedEvents


def fetch_events(url: str) -> GroupedEvents:
    return requests.get(url).json()
