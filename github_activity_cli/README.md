# GitHub User Activity CLI

A small command-line tool that fetches and displays a GitHub user's recent public activity.

This project uses GitHub's REST API:

```text
GET /users/{username}/events/public
```

## Requirements

- Python 3
- Internet connection

The project uses only Python's standard library, so no packages need to be installed.

## Usage

Run the script with a GitHub username:

```powershell
python github_user_activity_cli.py <username>
```

Example:

```powershell
python github_user_activity_cli.py octocat
```

## Example output

```text
Pushed 2 commit(s) to octocat/Hello-World (main branch)
Created branch feature-login in octocat/Hello-World
Opened issue #12: Fix login bug in octocat/Hello-World
Merged pull request #8: Add authentication in octocat/Hello-World
Starred octocat/Hello-World
Forked octocat/Hello-World into octocat/Hello-World-fork
```

## Supported events

The CLI currently formats these event types:

- `CommitCommentEvent`
- `PushEvent`
- `CreateEvent`
- `IssuesEvent`
- `PullRequestEvent`
- `WatchEvent`
- `ForkEvent`

Other event types are displayed using a basic fallback message.

## Notes

- Only public activity is returned.
- GitHub returns recent events, with the newest events first.
- A push event does not always include the commit count. For non-initial pushes, this project uses GitHub's compare API with the `before` and `head` commit IDs to calculate it.
- Unauthenticated GitHub API requests are subject to rate limits.
- The request includes a `User-Agent` header as recommended by GitHub.

## Error handling

The CLI reports:

- When the GitHub user does not exist
- HTTP errors returned by GitHub
- Network errors