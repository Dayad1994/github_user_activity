import sys

from gua.typing import GroupedEvents
from gua.fetcher import fetch_events
from gua.module import parse_events
from gua.view import print_events


URL = 'https://api.github.com/users/{username}/events'


def main() -> None:
    '''Start point of app.'''

    username: str = _get_username()
    full_url: str = URL.format(username=username)
    events: GroupedEvents = fetch_events(full_url)
    parse_events(events)
    print_events(events)


def _get_username() -> str:
    '''Get username from cli.'''

    username = 'dayanik'
    if len(sys.argv) > 1:
        username = sys.argv[1]
    return username


if __name__ == "__main__":
    main()
