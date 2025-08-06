from unittest.mock import patch, Mock

from gua.fetcher import fetch_events


@patch("gua.fetcher.requests.get")
def test_fetch_events(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            'id': 1,
            'type': 'CreateEvent',
            'actor': 'Actor',
            'repo': 'Repo',
            'payload': 'EventPayload',
            'public': True,
            'created_at': '06.08.2025 09:52',
            'org': 'EventOrg',
        }
    ]
    mock_get.return_value = mock_response
    
    url = 'https://api.github.com/users/dayanik/events'
    result = fetch_events(url)
    
    assert result == [
        {
            'id': 1,
            'type': 'CreateEvent',
            'actor': 'Actor',
            'repo': 'Repo',
            'payload': 'EventPayload',
            'public': True,
            'created_at': '06.08.2025 09:52',
            'org': 'EventOrg',
        }
    ]
