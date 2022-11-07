import pandas as pd
from github import Github
import json
import time
start = time.time()
g = Github("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")

df = pd.read_csv('repos.csv')

def update_star_count():
    for index, paper in df.iterrows():
        repo_url = paper['Name_Repo']
        repo = g.get_repo(repo_url)
        star = repo.stargazers_count
        if star != paper['Num_Star']:
            print(f'{index}.[{repo_url}] {star} != {paper["Num_Star"]}')
            df.loc[index, 'Num_Star'] = star
            df.to_csv('repos.csv', index=False)

def mine_issues():
    for index, paper in df.iterrows():
        repo_url = paper['Name_Repo']
        repo = g.get_repo(repo_url)
        issues = repo.get_issues()

        num_stars = repo.stargazers_count
        num_issue_open = sum(issue.pull_request is None for issue in issues)
        issue_labels = repo.get_labels()
        num_pr_open = issues.totalCount - num_issue_open
        num_issue_open_no_assignee = sum(issue.pull_request is None and issue.assignee is None for issue in issues)
        num_issue_open_no_label = sum(issue.pull_request is None and len(issue.labels) == 0 for issue in issues)
        used_labels = set()
        for issue in issues:
            used_labels.update(issue.labels)

        print(f'[{repo_url}]')
        print(f'Number of stars: {num_stars}')
        df.loc[index, 'Num_Star'] = num_stars
        print(f'Number of open issues: {num_issue_open}')
        df.loc[index, 'Num_Issue_Open'] = num_issue_open
        if num_issue_open > 0:
            print(
                f'Open issues with no assignee: {(num_issue_open_no_assignee / num_issue_open):.2%} ({num_issue_open_no_assignee})')
            df.loc[index, 'Num_Issue_Open_No_Assignee'] = int(num_issue_open_no_assignee)
            print(
                f'Open issues with no label: {(num_issue_open_no_label / num_issue_open):.2%} ({num_issue_open_no_label})')
            df.loc[index, 'Num_Issue_Open_No_Label'] = int(num_issue_open_no_label)
        print(f'Issue types: {"#".join([label.name for label in issue_labels])}')
        df.loc[index, 'Issue_Types'] = "#".join([label.name for label in issue_labels])
        print(f'Number of issue types: {issue_labels.totalCount}')
        df.loc[index, 'Num_Issue_Type'] = int(issue_labels.totalCount)
        if issue_labels.totalCount > 0:
            print(
                f'Unused issue types: {(issue_labels.totalCount - len(used_labels)) / issue_labels.totalCount:.2%} ({issue_labels.totalCount - len(used_labels)})')
            df.loc[index, 'Num_Issue_Type_Unused'] = int(issue_labels.totalCount - len(used_labels))
        else:
            df.loc[index, 'Num_Issue_Type_Unused'] = 0
        df.to_csv('repos.csv', index=False)

mine_issues()