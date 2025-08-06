"""Event handlers module."""

def _handle_commit_comment(payload: dict, repo_name: str) -> str:
    return f"Commented on a commit in {repo_name}"

def _handle_create(payload: dict, repo_name: str) -> str:
    ref_type = payload['ref_type']
    ref = payload.get('ref')
    if ref_type == 'repository':
        return f"Created {ref_type} {repo_name}"
    else:
        return f"Created {ref_type} {ref} in {repo_name}"

def _handle_delete(payload: dict, repo_name: str) -> str:
    ref_type = payload['ref_type']
    ref = payload['ref']
    return f"Deleted {ref_type} {ref} in {repo_name}"

def _handle_fork(payload: dict, repo_name: str) -> str:
    forked_repo_name = payload['forkee']['full_name']
    return f"Forked {repo_name} to {forked_repo_name}"

def _handle_gollum(payload: dict, repo_name: str) -> str:
    pages = payload['pages']
    return f"Updated wiki pages in {repo_name}: {pages}"

def _handle_issue_comment(payload: dict, repo_name: str) -> str:
    action = payload['action'].title()
    number = payload['issue']['number']
    return f"{action} a comment on an issue #{number} in {repo_name}"

def _handle_issues(payload: dict, repo_name: str) -> str:
    action = payload['action'].title()
    number = payload['issue']['number']
    return f"{action} an issue #{number} in {repo_name}"

def _handle_member(payload: dict, repo_name: str) -> str:
    action = payload['action'].lower()
    member = payload['member']['login']
    if action == 'added':
        return f"Added {member} as a collaborator in {repo_name}"
    else:
        return f"{action.title()} permissions for {member} in {repo_name}"

def _handle_public(payload: dict, repo_name: str) -> str:
    return f"Made {repo_name} public"

def _handle_pr(payload: dict, repo_name: str) -> str:
    action = payload['action'].title()
    number = payload['number']
    return f"{action} pull request #{number} in {repo_name}"

def _handle_pr_review(payload: dict, repo_name: str) -> str:
    action = payload['action'].title()
    number = payload['pull_request']['number']
    return f"{action} a review on pull request #{number} in {repo_name}"

def _handle_pr_review_comment(payload: dict, repo_name: str) -> str:
    action = payload['action'].lower()
    if action == 'created':
        return f"Commented on a pull request review in {repo_name}"
    else:
        return f"Updated comment on a pull request review in {repo_name}"

def _handle_pr_review_thread(payload: dict, repo_name: str) -> str:
    number = payload['pull_request']['number']
    return f"Updated a review thread in pull request #{number} in {repo_name}"

def _handle_release(payload: dict, repo_name: str) -> str:
    action = payload['action'].title()
    name = payload['release']['name']
    return f"{action} release {name} in {repo_name}"

def _handle_sponsorship(payload: dict, repo_name: str) -> str:
    action = payload['action'].title()
    user = payload['sponsorship']['sponsorable']['name']
    return f"{action} sponsorship for {user}"

def _handle_watch(payload: dict, repo_name: str) -> str:
    return f"Starred {repo_name}"
