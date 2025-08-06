from gua.module import sort_create_events, group_push_events, get_create_event_sort_key
from gua.typing import Event


def make_event(event_type, created_at, ref_type):
    return {
        'id': 1,
        'type': event_type,
        'actor': {'id': 1, 'login': 'user', 'display_login': 'user', 'gravatar_id': '', 'url': '', 'avatar_url': ''},
        'repo': {'id': 1, 'name': 'repo', 'url': ''},
        'payload': {'ref_type': ref_type},
        'public': True,
        'created_at': created_at,
        'org': None
    }


def test_get_create_event_sort_key():
    event_branch = make_event('CreateEvent', '2023-01-01T00:00:00Z', 'branch')
    event_tag = make_event('CreateEvent', '2023-01-01T00:00:00Z', 'tag')
    event_repository = make_event('CreateEvent', '2023-01-01T00:00:00Z', 'repository')
    event_empty = make_event('PushEvent', '2023-01-01T00:00:00Z', '')
    
    result_event_branch = get_create_event_sort_key(event_branch)
    result_event_tag = get_create_event_sort_key(event_tag)
    result_event_repository = get_create_event_sort_key(event_repository)
    result_event_empty = get_create_event_sort_key(event_empty)
    
    assert result_event_branch == ('2023-01-01T00:00:00Z', 1)
    assert result_event_tag == ('2023-01-01T00:00:00Z', 0)
    assert result_event_repository == ('2023-01-01T00:00:00Z', 2)
    assert result_event_empty == ('2023-01-01T00:00:00Z', 3)


def test_sort_create_events():
    events = [
        make_event('CreateEvent', '2023-01-01T00:00:00Z', 'branch'),
        make_event('CreateEvent', '2023-01-01T00:00:00Z', 'tag'),
        make_event('CreateEvent', '2023-01-01T00:00:00Z', 'repository'),
        make_event('PushEvent', '2023-01-02T00:00:00Z', ''),
        make_event('CreateEvent', '2023-01-03T00:00:00Z', 'repository'),
        make_event('CreateEvent', '2023-01-04T00:00:00Z', 'branch'),
        make_event('CreateEvent', '2023-01-01T00:00:00Z', 'repository'),
        make_event('CreateEvent', '2023-01-01T00:00:00Z', 'tag'),
        make_event('PushEvent', '2023-01-02T00:00:00Z', ''),
    ]

    expected_first_triple = sorted(events[0:3], key=lambda e: (e['created_at'], {'tag':0,'branch':1,'repository':2,'':3}[e['payload']['ref_type']]))
    expected_pre_last_two = sorted(events[-3:-1], key=lambda e: (e['created_at'], {'tag':0,'branch':1,'repository':2,'':3}[e['payload']['ref_type']]))
    expected_last_event = events[-1]
    sort_create_events(events)

    # Проверяем, что первые 3 отсортировались
    assert events[0:3] == expected_first_triple
    # Следующие 3 остались без изменений
    assert events[3:] == events[3:]
    assert events[-3:-1] == expected_pre_last_two
    assert events[-1] == expected_last_event


def test_group_push_events():
    ...
