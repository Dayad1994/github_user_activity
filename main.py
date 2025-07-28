import requests


def sort_create_events(events):
    def inner_sort():
        for i in range(1, len(events)):
            event = events[i]
            prev_event = events[i - 1]
            if event['type'] == 'CreateEvent' and prev_event['type'] == 'CreateEvent':
                if event['created_at'] == prev_event['created_at']:
                    if event['payload']['ref_type'] == 'branch' and prev_event['payload']['ref_type'] == 'repository':
                        events[i], events[i-1] = events[i-1], events[i]
                    elif event['payload']['ref_type'] == 'tag' and prev_event['payload']['ref_type'] == 'branch':
                        events[i], events[i-1] = events[i-1], events[i]
                    elif event['payload']['ref_type'] == 'tag' and prev_event['payload']['ref_type'] == 'repository':
                        events[i], events[i-1] = events[i-1], events[i]
    inner_sort()
    inner_sort()


def main(url: str = 'https://api.github.com/users/{username}/events',
         username: str = 'sobolevn'):
    full_url = url.format(username=username)
    events = requests.get(full_url).json()
    
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
    elif event['type'] == 'WatchEvent':
        print(f'Starred {event['repo']['name']}')
    else:
        print(event['type'], event['repo']['name'])


if __name__ == "__main__":
    main()
