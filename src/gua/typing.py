"""Type hints module."""

from enum import Enum
from typing import TypedDict


class EventActor(TypedDict):
    id: int
    login: str
    display_login: str
    gravatar_id: str
    url: str
    avatar_url: str


class EventRepo(TypedDict):
    id: int
    name: str
    url: str


class EventOrg(TypedDict):
    id: int
    login: str
    gravatar_id: str
    url: str
    avatar_url: str


class EventPayload(TypedDict):
    ref_type: str


class Event(TypedDict):
    id: int
    type: str
    actor: EventActor
    repo: EventRepo
    payload: EventPayload
    public: bool
    created_at: str
    org: EventOrg | None


GroupedEvents = list[Event | tuple[Event, int]]

'''
class EventType(str, Enum):
    Push = 'CommitCommentEvent'
    Create = 'CreateEvent'
    Delete = 'DeleteEvent'
    Fork = 'ForkEvent'
    Gollum = 'GollumEvent'
    IssueComment = 'IssueCommentEvent'
    Issues = 'IssuesEvent'
    Member = 'MemberEvent'
    Public = 'PublicEvent'
    PullRequest = 'PullRequestEvent'
    PullRequestReview = 'PullRequestReviewEvent'
    PullRequestReviewComment = 'PullRequestReviewCommentEvent'
    PullRequestReviewThread = 'PullRequestReviewThreadEvent'
    Release = 'ReleaseEvent'
    Sponsorship = 'SponsorshipEvent'
    Watch = 'WatchEvent'
'''
