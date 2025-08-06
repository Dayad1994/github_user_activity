"""Fetch data module."""

import requests

from gua.typing import GroupedEvents


def fetch_events(url: str) -> GroupedEvents:
    """Get last github user events."""
    return requests.get(url, timeout=(3.05, 10)).json()
