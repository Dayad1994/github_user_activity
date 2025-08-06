"""Fetch data module."""

import requests

from gua.typing import GroupedEvents


def fetch_events(url: str) -> GroupedEvents:
    """Get last github user events."""
    try:
        response = requests.get(url, timeout=(3.05, 10))
        if response.status_code == 200:
            return response.json()
        else:
            return 'User with that username does not exist.'
    except TimeoutError:
        return 'Server is unavailable. Please try again later.'
    except Exception:
        return 'Something goes wrong. Please try again later.'
