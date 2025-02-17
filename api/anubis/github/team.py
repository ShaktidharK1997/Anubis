from anubis.github.api import github_rest


def list_github_team_members(org: str, team: str) -> list[str]:
    return [
        user['login']
        for user in github_rest(f"/orgs/{org}/teams/{team}/members")
        if 'login' in user
    ]


def add_github_team_member(org: str, team: str, username: str):
    github_rest(f"/orgs/{org}/teams/{team}/memberships/{username}", method="put")


def remote_github_team_member(org: str, team: str, username: str):
    github_rest(f"/orgs/{org}/teams/{team}/memberships/{username}", method="delete")
