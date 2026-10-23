from argparse import ArgumentParser
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

parser = ArgumentParser()
parser.add_argument('username', help='The GitHub username to check activity of', type=str)

args = parser.parse_args()

url = f"https://api.github.com/users/{args.username}/events/public"

try:
    request = Request(
        url,
        headers={"User-Agent": "github-user-activity-cli"}
    )
    with urlopen(request) as response:
        body = response.read()

except HTTPError as error:
    if error.code == 404:
        print(f"User {args.username} does not exist.")
    else:
        print(f"GitHub returned HTTP {error.code}")
    raise SystemExit(1)
except URLError as error:
    print(f"Network Error: {error.reason}")
    raise SystemExit(1)


events = json.loads(body)

# to get commit count from github compare api
def get_commit_count(repo_name, before, head):
    compare_url = (
        f"https://api.github.com/repos/{repo_name}/compare/"
        f"{before}...{head}"
    )

    request = Request(
        compare_url,
        headers={"User-Agent": "github-user-activity-cli"}
    )

    with urlopen(request) as response:
        comparison = json.loads(response.read())

    return comparison["total_commits"]

for event in events:
    
    if event['type'] == 'CommitCommentEvent':
        print(f"Performed {event['payload']['action']} with comment - {event['payload']['comment']}")
    
    elif event['type'] == 'PushEvent':
        payload = event["payload"]
        repository = event["repo"]["name"]

        before = payload["before"]
        head = payload["head"]
        branch = payload["ref"].removeprefix("refs/heads/")

        # if initial commit then before will be all 0
        if before == "0" * 40:
            print(f"Pushed commits to {repository} ({branch} branch)")
        else:
            commit_count = get_commit_count(repository, before, head)
            print(
                f"Pushed {commit_count} commit(s) "
                f"to {repository} ({branch} branch)"
            )

    elif event['type'] == 'CreateEvent':
        payload = event['payload']
        repository = event['repo']['name']
        ref_type = event['payload']['ref_type']
        
        if ref_type == 'repository': # ref_type can be branch, tag or repository
            print(f"Created repository {repository}")
        else:
            ref_name = payload.get("ref") # it is git ref resource branch

            if ref_name is None:
                full_ref = payload.get("full_ref", "")
                ref_name = full_ref.split('/')[-1]

            print(f"Created {ref_type} {ref_name} in {repository}")

    elif event['type'] == 'IssuesEvent':
        payload = event['payload']
        issue = payload['issue']
        action = payload['action']

        print(
            f"{action.capitalize()} issue #{issue['number']}: "
            f"{issue['title']} in {event['repo']['name']}"
        )

    elif event['type'] == 'PullRequestEvent':
        payload = event["payload"]
        pull_request = payload["pull_request"]
        action = payload["action"]
        repository = event["repo"]["name"]

        if action == "closed" and pull_request["merged"]:
            action_text = "Merged"
        else:
            action_text = action.capitalize()

        print(
            f"{action_text} pull request "
            f"#{pull_request['number']}: "
            f"{pull_request['title']} in {repository}"
        )

    elif event['type'] == 'WatchEvent':
        print(f"Starred {event['repo']['name']}")

    elif event['type'] == 'ForkEvent':
        payload = event["payload"]
        repository = event["repo"]["name"]
        fork = payload["forkee"]["full_name"]

        print(f"Forked {repository} into {fork}")
    else:
        print(f"{event['type']} in {event['repo']['name']}")