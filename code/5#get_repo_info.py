import pandas as pd
from github_token import *
repo_input_src = 'repoDB.csv'
repo_output_src = 'repoDB.csv'
issue_src = 'issueDB.csv'

name_to_record = ""
start = True

repo_set = set()

df_repo = pd.read_csv(repo_input_src)
for index, paper in df_repo.iterrows():
    df_issue = pd.DataFrame()
    if paper['Name_Repo'] == name_to_record: start = True
    if not start: continue
    print(f'[{index + 1}] {paper["Name_Repo"]}')
    repo_url = paper['Name_Repo']
    # Tolerant nested repo
    if len(repo_url.split('/')) != 2:
        repo_url = repo_url.split('/')[0] + '/' + repo_url.split('/')[1]
        print(f'Nested repo: {repo_url}')
    if repo_url in repo_set:
        print(f'Repo {repo_url} already recorded')
        continue
    repo = g.get_repo(repo_url)
    repo_set.add(repo_url)
    # Open issues includes open issues and PRs.
    open_issues = repo.get_issues(state="open")
    closed_issues = repo.get_issues(state="closed")

    num_stars = repo.stargazers_count
    num_forks = repo.forks_count
    num_watchers = repo.subscribers_count
    contributors = repo.get_contributors()

    count = 0
    for issues in [open_issues, closed_issues]:
        for issue in issues:
            remaining_limit = 0
            while remaining_limit < 100:
                try:
                    remaining_limit = g.get_rate_limit().core.remaining
                except Exception as e:
                    remaining_limit = 0
            print(f'-{count}- {issue.pull_request}')
            count += 1

    num_issue_open = sum(issue.pull_request is None for issue in open_issues)
    num_issue_closed = sum(issue.pull_request is None for issue in closed_issues)
    issue_labels = repo.get_labels()
    #num_pr_open = open_issues.totalCount - num_issue_open
    #num_pr_closed = closed_issues.totalCount - num_issue_closed

    #May need to verify
    num_issue_open_no_assignee = sum(issue.pull_request is None and issue.assignee is None for issue in open_issues)
    num_issue_open_no_label = sum(issue.pull_request is None and len(issue.labels) == 0 for issue in open_issues)
    num_issue_closed_no_assignee = sum(issue.pull_request is None and issue.assignee is None for issue in closed_issues)
    num_issue_closed_no_label = sum(issue.pull_request is None and len(issue.labels) == 0 for issue in closed_issues)

    used_labels = set()
    issue_list = []

    # Handle Issue DB
    for issues in [open_issues, closed_issues]:
        for issue in issues:
            row_num = len(df_issue) - 1
            print(row_num)
            if issue.pull_request is None:
                print(issue.assignees)
                print(issue.title)
                df_issue.loc[row_num, 'Title'] = issue.title
                df_issue.loc[row_num, 'Name_Repo'] = repo_url
                df_issue.loc[row_num, 'State'] = issue.state
                df_issue.loc[row_num, 'Assignees'] = "\n".join(assignee._identity for assignee in issue.assignees)
                df_issue.loc[row_num, 'Proposed_By'] = issue.user._identity
                df_issue.loc[row_num, 'Closed_By'] = issue.closed_by._identity if issue.closed_by is not None else None
                df_issue.loc[row_num, 'Date_Created'] = issue.created_at
                df_issue.loc[row_num, 'Date_Closed'] = issue.closed_at
                df_issue.loc[row_num, 'Num_Comment'] = issue.comments
                df_issue.loc[row_num, 'Label_Issue'] = "#".join([label.name for label in issue.labels])
                df_issue.loc[row_num, 'Identity_Repo'] = issue._identity
                df_issue.loc[row_num, 'Identity_Global'] = issue.id
                df_issue.loc[row_num, 'Body'] = issue.body
                issue_list.append(str(issue._identity))
            used_labels.update(issue.labels)

    # Handle Repo DB
    df_repo.loc[index, 'Issue_Types'] = "#".join([label.name for label in issue_labels])
    df_repo.loc[index, 'IDList_Issue'] = "#".join(issue_list)

    print(f'[{repo_url}]')
    print(f'Number of stars: {num_stars}')
    df_repo.loc[index, 'Num_Star'] = num_stars

    print(f'Number of forks: {num_forks}')
    df_repo.loc[index, 'Num_Fork'] = num_forks

    print(f'Number of watchers: {num_watchers}')
    df_repo.loc[index, 'Num_Watcher'] = num_watchers

    print(f'Created at: {repo.created_at}')
    df_repo.loc[index, 'Date_Created'] = repo.created_at

    print(f'Last updated at: {repo.updated_at}')
    df_repo.loc[index, 'Date_Last_Mod'] = repo.updated_at

    print(f'Number of issues: {num_issue_open}')
    df_repo.loc[index, 'Num_Issue'] = num_issue_open + num_issue_closed

    print(f'Number of issue types: {issue_labels.totalCount}')
    df_repo.loc[index, 'Num_Issue_Type'] = issue_labels.totalCount

    print(f'Number of open issues: {num_issue_open}')
    df_repo.loc[index, 'Num_Issue_Open'] = num_issue_open

    print(f'Number of closed issues: {num_issue_closed}')
    df_repo.loc[index, 'Num_Issue_Closed'] = num_issue_closed

    print(f'Contributors: ')
    df_repo.loc[index, 'Contributors'] = "\n".join([_._identity for _ in contributors])

    if num_issue_open > 0:
        print(
            f'Open issues with no assignee: {(num_issue_open_no_assignee / num_issue_open):.2%} ({num_issue_open_no_assignee})')
        df_repo.loc[index, 'Num_Issue_Open_No_Assignee'] = int(num_issue_open_no_assignee)
        print(
            f'Open issues with no label: {(num_issue_open_no_label / num_issue_open):.2%} ({num_issue_open_no_label})')
        df_repo.loc[index, 'Num_Issue_Open_No_Label'] = int(num_issue_open_no_label)

    if num_issue_closed > 0:
        print(
            f'Closed issues with no assignee: {(num_issue_closed_no_assignee / num_issue_closed):.2%} ({num_issue_closed_no_assignee})')
        df_repo.loc[index, 'Num_Issue_Closed_No_Assignee'] = int(num_issue_closed_no_assignee)
        print(
            f'Closed issues with no label: {(num_issue_closed_no_label / num_issue_closed):.2%} ({num_issue_closed_no_label})')
        df_repo.loc[index, 'Num_Issue_Closed_No_Label'] = int(num_issue_closed_no_label)

    if issue_labels.totalCount > 0:
        print(f'Unused issue types: {(issue_labels.totalCount - len(used_labels)) / issue_labels.totalCount:.2%} ({issue_labels.totalCount - len(used_labels)})')

        df_repo.loc[index, 'Num_Issue_Type_Unused'] = int(issue_labels.totalCount - len(used_labels))
    else:
        df_repo.loc[index, 'Num_Issue_Type_Unused'] = 0

    df_repo.to_csv(repo_output_src, index=False)
    df_issue.to_csv(issue_src, index=False, mode='a', header=False)
