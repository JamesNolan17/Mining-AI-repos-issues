import pandas as pd
from github_token import *

df_repo = pd.read_csv('repoDB.csv')
df_issue = pd.read_csv('issueDB.csv')


print(len(df_issue))
for index, paper in df_repo.iterrows():
    repo_name = paper['Name_Repo']
    issue_string = str(paper['IDList_Issue'])
    if issue_string == 'nan':
        issue_list = []
    else:
        issue_list = sorted([int(i) for i in issue_string.split('#')])
    #print(issue_list)
    issue_df = df_issue.query(f"`Name_Repo` == '{repo_name}'")['Identity_Repo']
    issue_list_real = sorted([int(i) for i in issue_df.tolist()])
    if issue_list_real != issue_list:
        issue_list_real.sort()
        issue_list.sort()
        print(repo_name)
        repo = g.get_repo(repo_name)
        issues_number = repo.get_issues(state="open").totalCount + repo.get_issues(state="closed").totalCount
        if len(issue_list_real) != issues_number:
            print(f'Issue number mismatch: {len(issue_list_real)} vs {issues_number}')
            print(f'Issue list recorded in repoDB: {len(issue_list)}-{issue_list}')
            print(f'Issue list recorded in issueDB: {len(issue_list_real)}-{issue_list_real}')
        else:
            df_repo.loc[index, 'IDList_Issue'] = '#'.join([str(i) for i in issue_list_real])
        for i in range(len(issue_list)):
            if issue_list[i] != issue_list_real[i]:
                print(f'Index {i}: {issue_list[i]}-{issue_list_real[i]}')