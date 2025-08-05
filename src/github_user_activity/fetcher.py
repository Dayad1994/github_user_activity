"""Fetch data module."""

import requests

from github_user_activity.event_types import GroupedEvents


def fetch_events(url: str) -> GroupedEvents:
    return requests.get(url).json()
