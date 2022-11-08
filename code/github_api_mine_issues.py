import pandas as pd
from github import Github
import json
import time
start = time.time()
g = Github("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")
df_repo = pd.read_csv('repoDB.csv')
df_issue = pd.read_csv('issueDB.csv')

first_to_record = "mnswdhw/InvGAN-Pytorch"

for index, paper in df_repo.iterrows():
    repo_url = paper['Name_Repo']
    try:
        repo = g.get_repo(repo_url)
    except Exception as e:
        print(repo_url)
        print(f'{e}')
        time.sleep(60*60)
        continue
    issues = repo.get_issues()

    num_stars = repo.stargazers_count
    num_issue_open = sum(issue.pull_request is None for issue in issues)
    issue_labels = repo.get_labels()
    num_pr_open = issues.totalCount - num_issue_open
    num_issue_open_no_assignee = sum(issue.pull_request is None and issue.assignee is None for issue in issues)
    num_issue_open_no_label = sum(issue.pull_request is None and len(issue.labels) == 0 for issue in issues)
    used_labels = set()
    issue_list = []
    for issue in issues:
        row_num = len(df_issue)-1
        print(row_num)
        if issue.pull_request is None:
            print(issue.title)
            df_issue.loc[row_num, 'Title'] = issue.title
            df_issue.loc[row_num, 'Name_Repo'] = repo_url
            df_issue.loc[row_num, 'Date_Created'] = issue.created_at
            print(issue.comments) # number of comments
            df_issue.loc[row_num, 'Num_Comment'] = issue.comments
            print(issue.labels)
            df_issue.loc[row_num, 'Label_Issue'] = "#".join([label.name for label in issue.labels])
            print(issue._identity)
            df_issue.loc[row_num, 'Identity_Repo'] = issue._identity
            df_issue.loc[row_num, 'Identity_Global'] = issue.id
            df_issue.loc[row_num, 'Body'] = issue.body
            issue_list.append(str(issue._identity))
        used_labels.update(issue.labels)
    df_repo.loc[index, 'IDList_Issue'] = "#".join(issue_list)

    print(f'[{repo_url}]')
    print(f'Number of stars: {num_stars}')
    df_repo.loc[index, 'Num_Star'] = num_stars
    print(f'Number of open issues: {num_issue_open}')
    df_repo.loc[index, 'Num_Issue_Open'] = num_issue_open
    print(f'Number of open PRs: {num_pr_open}')
    df_repo.loc[index, 'Num_PR_Open'] = num_pr_open
    if num_issue_open > 0:
        print(
            f'Open issues with no assignee: {(num_issue_open_no_assignee / num_issue_open):.2%} ({num_issue_open_no_assignee})')
        df_repo.loc[index, 'Num_Issue_Open_No_Assignee'] = int(num_issue_open_no_assignee)
        print(
            f'Open issues with no label: {(num_issue_open_no_label / num_issue_open):.2%} ({num_issue_open_no_label})')
        df_repo.loc[index, 'Num_Issue_Open_No_Label'] = int(num_issue_open_no_label)
    print(f'Issue types: {"#".join([label.name for label in issue_labels])}')
    df_repo.loc[index, 'Issue_Types'] = "#".join([label.name for label in issue_labels])
    print(f'Number of issue types: {issue_labels.totalCount}')
    df_repo.loc[index, 'Num_Issue_Type'] = int(issue_labels.totalCount)
    if issue_labels.totalCount > 0:
        print(
            f'Unused issue types: {(issue_labels.totalCount - len(used_labels)) / issue_labels.totalCount:.2%} ({issue_labels.totalCount - len(used_labels)})')
        df_repo.loc[index, 'Num_Issue_Type_Unused'] = int(issue_labels.totalCount - len(used_labels))
    else:
        df_repo.loc[index, 'Num_Issue_Type_Unused'] = 0

    df_repo.to_csv('repoDB.csv', index=False)
    df_issue.to_csv('issueDB.csv', index=False)
