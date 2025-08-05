"""Fetch data module."""

import requests

from github_user_activity.event_types import Event


def fetch_events(url: str) -> list[Event]:
    return requests.get(url).json()
