import requests
import sys

from typing import TypedDict


class EventActor(TypedDict):
    id: int
    login: str
    display_login: str
    gravatar_id: str
    url: str
    avatart_url: str


class EventRepo(TypedDict):
    id: int
    name: str
    url: str


class EventOrg(TypedDict):
    id: int
    login: str
    gravatar_id: str
    url: str
    avatart_url: str


class EventPayload(TypedDict):
    ...


class Event(TypedDict):
    id: int
    type: str
    actor: EventActor
    repo: EventRepo
    payload: EventPayload
    public: bool
    created_at: str
    org: EventOrg | None


TYPE_WEIGHTS = {
    'tag': 0,
    'branch': 1,
    'repository': 2,
    '': 3
}


def main(url: str = 'https://api.github.com/users/{username}/events',
         username: str = 'sobolevn'):
    full_url = url.format(username=username)
    events: list[Event] = requests.get(full_url).json()
    
    sort_create_events(events)
    
    # grouping same pushevents
    pushevent_repo_name = None
    pushevent = None
    same_events_count = 0
    
    for event in events:
        if event['type'] == 'PushEvent':
            if pushevent_repo_name == event['repo']['name']:
                same_events_count += 1
            else:
                if same_events_count:
                    print_event(pushevent, same_events_count)
                same_events_count = 1
                pushevent_repo_name = event['repo']['name']
                pushevent = event
        else:
            if same_events_count:
                print_event(pushevent, same_events_count)
            print_event(event)
            
            same_events_count = 0
            pushevent_repo_name = None


def sort_create_events(events: list[Event]):
    '''Сортировка событий CreateEvent.
    
    При создании репозитория генерируются два события: создание репозитория и создание главной ветки.
    Бывает, что у этих двух событий одна временная метка.
    И в таком случае github возвращает эти события отсортировав по имени события.
    А для корректного отображения событий важен логический порядок: репозиторий, ветка, тег. 
    '''

    for index in range(2, len(events)):
        triple_e = events[index - 2:index + 1]

        triple_e_types = [e['type'] for e in triple_e]
        triple_e_dates = [e['created_at'] for e in triple_e]

        if triple_e_types.count('CreateEvent') <= 1:
            continue

        if len(set(triple_e_dates)) == 3:
            continue

        triple_e.sort(key=_get_create_event_sort_key)
        events[index - 2:index + 1] = triple_e


def _get_create_event_sort_key(event):
    event_date = event['created_at']
    event_ref_type = event['payload'].get('ref_type', '')
    return event_date, TYPE_WEIGHTS[event_ref_type]


def print_event(event, commit_count=0):
    repo_name = event['repo']['name']
    
    if commit_count:
        commit_word = "commit" if commit_count == 1 else "commits"
        print(f"Pushed {commit_count} {commit_word} to {repo_name}")
    
    elif event['type'] == 'CommitCommentEvent':
        print(f'Commented on a commit in {repo_name}')
    
    elif event['type'] == 'CreateEvent':
        ref_type = event['payload']['ref_type']
        if ref_type == 'repository':
            print(f'Created {ref_type} {repo_name}')
        else:
            ref = event['payload']['ref']
            print(f'Created {ref_type} {ref} in {repo_name}')
    
    elif event['type'] == 'DeleteEvent':
        ref_type = event['payload']['ref_type']
        ref = event['payload']['ref']
        print(f'Deleted {ref_type} {ref} in {repo_name}')
    
    elif event['type'] == 'ForkEvent':
        forked_repo_name = event['payload']['forkee']['full_name']        
        print(f'Forked {repo_name} to {forked_repo_name}')
    
    elif event['type'] == 'GollumEvent':
        pages = event['payload']['pages']        
        print(f'Updated wiki pages in {repo_name}: {pages}')
    
    elif event['type'] == 'IssueCommentEvent':
        action = event['payload']['action'].title()
        issue_number = event['payload']['issue']['number']        
        print(f'{action} a comment on an issue #{issue_number} in {repo_name}')
    
    elif event['type'] == 'IssuesEvent':
        action = event['payload']['action'].title()
        issue_number = event['payload']['issue']['number']        
        print(f'{action} an issue #{issue_number} in {repo_name}')
    
    elif event['type'] == 'MemberEvent':
        action = event['payload']['action'].title()
        member = event['payload']['member']['login']
        if action == 'added':
            print(f'{action} {member} as a collaborator in {repo_name}')
        else:
            print(f'{action} permissions for {member} in {repo_name}')
    
    elif event['type'] == 'PublicEvent':
        print(f'Made {repo_name} public')
    
    elif event['type'] == 'PullRequestEvent':
        action = event['payload']['action'].title()
        pr_number = event['payload']['number']
        print(f'{action} pull request #{pr_number} in {repo_name}')
    
    elif event['type'] == 'PullRequestReviewEvent':
        action = event['payload']['action'].title()
        pr_number = event['payload']['pull_request']['number']
        print(f'{action} a review on pull request #{pr_number} in {repo_name}')
    
    elif event['type'] == 'PullRequestReviewCommentEvent':
        action = event['payload']['action'].title()
        if action == 'created':
            print(f'Commented on a pull request review in {repo_name}')
        else:
            print(f'Updated comment on a pull request review in {repo_name}')
    
    elif event['type'] == 'PullRequestReviewThreadEvent':
        action = event['payload']['action'].title()
        pr_number = event['payload']['pull_request']['number']
        print(f'Updated a review thread in pull request #{pr_number} in {repo_name}')

    elif event['type'] == 'ReleaseEvent':
        action = event['payload']['action'].title()
        release_name = event['payload']['release']['name']
        print(f'{action} release {release_name} in {repo_name}')

    elif event['type'] == 'SponsorshipEvent':
        action = event['payload']['action'].title()
        sponsored_user = event['payload']['sponsorship']['sponsorable']['name']
        print(f'{action} sponsorship for {sponsored_user}')

    elif event['type'] == 'WatchEvent':
        print(f'Starred {event['repo']['name']}')
    else:
        print(event['type'], event['repo']['name'])


if __name__ == "__main__":
    username = sys.argv[1]
    main(username=username)
