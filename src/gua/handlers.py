"""Event handlers module."""

def _handle_commit_comment(payload: dict, repo_name: str):
    print(f"Commented on a commit in {repo_name}")

def _handle_create(payload: dict, repo_name: str):
    ref_type = payload['ref_type']
    ref = payload.get('ref')
    if ref_type == 'repository':
        print(f"Created {ref_type} {repo_name}")
    else:
        print(f"Created {ref_type} {ref} in {repo_name}")

def _handle_delete(payload: dict, repo_name: str):
    ref_type = payload['ref_type']
    ref = payload['ref']
    print(f"Deleted {ref_type} {ref} in {repo_name}")

def _handle_fork(payload: dict, repo_name: str):
    forked_repo_name = payload['forkee']['full_name']
    print(f"Forked {repo_name} to {forked_repo_name}")

def _handle_gollum(payload: dict, repo_name: str):
    pages = payload['pages']
    print(f"Updated wiki pages in {repo_name}: {pages}")

def _handle_issue_comment(payload: dict, repo_name: str):
    action = payload['action'].title()
    number = payload['issue']['number']
    print(f"{action} a comment on an issue #{number} in {repo_name}")

def _handle_issues(payload: dict, repo_name: str):
    action = payload['action'].title()
    number = payload['issue']['number']
    print(f"{action} an issue #{number} in {repo_name}")

def _handle_member(payload: dict, repo_name: str):
    action = payload['action'].lower()
    member = payload['member']['login']
    if action == 'added':
        print(f"Added {member} as a collaborator in {repo_name}")
    else:
        print(f"{action.title()} permissions for {member} in {repo_name}")

def _handle_public(payload: dict, repo_name: str):
    print(f"Made {repo_name} public")

def _handle_pr(payload: dict, repo_name: str):
    action = payload['action'].title()
    number = payload['number']
    print(f"{action} pull request #{number} in {repo_name}")

def _handle_pr_review(payload: dict, repo_name: str):
    action = payload['action'].title()
    number = payload['pull_request']['number']
    print(f"{action} a review on pull request #{number} in {repo_name}")

def _handle_pr_review_comment(payload: dict, repo_name: str):
    action = payload['action'].lower()
    if action == 'created':
        print(f"Commented on a pull request review in {repo_name}")
    else:
        print(f"Updated comment on a pull request review in {repo_name}")

def _handle_pr_review_thread(payload: dict, repo_name: str):
    number = payload['pull_request']['number']
    print(f"Updated a review thread in pull request #{number} in {repo_name}")

def _handle_release(payload: dict, repo_name: str):
    action = payload['action'].title()
    name = payload['release']['name']
    print(f"{action} release {name} in {repo_name}")

def _handle_sponsorship(payload: dict, repo_name: str):
    action = payload['action'].title()
    user = payload['sponsorship']['sponsorable']['name']
    print(f"{action} sponsorship for {user}")

def _handle_watch(payload: dict, repo_name: str):
    print(f"Starred {repo_name}")
