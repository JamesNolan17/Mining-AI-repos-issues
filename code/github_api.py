from github import Github
import json
import time
start = time.time()
from google_scholar_api import query

g = Github("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")

with open('repos.json') as f:
    repos = json.load(f)
# repos = {"Transformers": "https://github.com/huggingface/transformers"}

star_dataset = {}
issue_dataset = {}
issue_type_dataset = {}
for repo_url in repos.values():
    if repo_url.startswith('https://github.com/'):
        repo_url = repo_url.replace('https://github.com/', '')
        try:
            repo = g.get_repo(repo_url)
            star_dataset[repo_url] = repo.stargazers_count
            issue_dataset[repo_url] = repo.get_issues()
            issue_type_dataset[repo_url] = repo.get_labels()
            print(f'[{repo_url}] {repo.get_issues().totalCount}')
        except Exception as e:
            print(f'[{repo_url}] {e}')

# Analysis Issue Stats

for repo_url, issues in issue_dataset.items():
    num_issue_open = sum(issue.pull_request is None for issue in issues)
    num_pr_open = issues.totalCount - num_issue_open
    num_issue_open_no_assignee = sum(issue.pull_request is None and issue.assignee is None for issue in issues)
    num_issue_open_no_label = sum(issue.pull_request is None and len(issue.labels) == 0 for issue in issues)
    num_issue_type = issue_type_dataset[repo_url].totalCount
    used_labels = set()
    for issue in issues:
        used_labels.update(issue.labels)

    print(f'[{repo_url}]')
    print(f'Number of stars: {star_dataset[repo_url]}')
    print(f'Number of open issues: {num_issue_open}')
    if num_issue_open > 0:
        print(f'Open issues with no assignee: {(num_issue_open_no_assignee / num_issue_open):.2%} ({num_issue_open_no_assignee})')
        print(f'Open issues with no label: {(num_issue_open_no_label / num_issue_open):.2%} ({num_issue_open_no_label})')
    print(f'Number of issue types: {num_issue_type}')
    if num_issue_type > 0:
        print(f'Unused issue types: {(num_issue_type - len(used_labels)) / num_issue_type:.2%} ({num_issue_type - len(used_labels)})')

print(f'Average issue per repo: {sum(sum(issue.pull_request is None for issue in issues) for issues in issue_dataset.values()) / len(issue_dataset.keys())}')
print(f'----------------------\nTime: {int(time.time() - start)}s')
