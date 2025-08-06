from typing import Callable

from gua import handlers
from gua.event_types import Event, GroupedEvents


# Сопоставление типов событий и обработчиков
EVENT_HANDLERS: dict[str, Callable[[], None]] = {
        'CommitCommentEvent': handlers._handle_commit_comment,
        'CreateEvent': handlers._handle_create,
        'DeleteEvent': handlers._handle_delete,
        'ForkEvent': handlers._handle_fork,
        'GollumEvent': handlers._handle_gollum,
        'IssueCommentEvent': handlers._handle_issue_comment,
        'IssuesEvent': handlers._handle_issues,
        'MemberEvent': handlers._handle_member,
        'PublicEvent': handlers._handle_public,
        'PullRequestEvent': handlers._handle_pr,
        'PullRequestReviewEvent': handlers._handle_pr_review,
        'PullRequestReviewCommentEvent': handlers._handle_pr_review_comment,
        'PullRequestReviewThreadEvent': handlers._handle_pr_review_thread,
        'ReleaseEvent': handlers._handle_release,
        'SponsorshipEvent': handlers._handle_sponsorship,
        'WatchEvent': handlers._handle_watch,
    }


def print_events(events: GroupedEvents) -> None:
    '''Print all events.
    
    В зависимости от типа (event или кортеж(event, count)) очередного элемента списка
    вызывается print_event() с одним или двумя аргументами.
    '''

    for event in events:
        if isinstance(event, tuple):
            print_event(event=event[0], commit_count=event[1])
        else:
            print_event(event)


def print_event(event: Event, commit_count: int = 0) -> None:
    """Print event short description."""

    event_type = event['type']
    repo_name = event['repo']['name']
    payload = event.get('payload', {})

    if commit_count:
        commit_word = "commit" if commit_count == 1 else "commits"
        print(f"Pushed {commit_count} {commit_word} to {repo_name}")
        return

    # Вызов обработчика или вывод по умолчанию
    handler = EVENT_HANDLERS.get(event_type)
    if handler:
        handler(payload, repo_name)
    else:
        print(event_type, repo_name)
