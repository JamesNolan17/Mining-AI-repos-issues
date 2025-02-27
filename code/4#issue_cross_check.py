import pandas as pd
from github_token import *

df_repo = pd.read_csv('repoDB.csv')
df_issue = pd.read_csv('issueDB.csv')


print(len(df_issue))
for index, paper in df_repo.iterrows():
    repo_name = paper['Name_Repo'].split('/')[0] + '/' + paper['Name_Repo'].split('/')[1]
    issue_string = str(paper['IDList_Issue'])
    if issue_string == 'nan':
        issue_list = []
    else:
        issue_list = sorted([int(i) for i in issue_string.split('#')])
    #print(issue_list)
    issue_df = df_issue.query(f"`Name_Repo` == '{repo_name}'")['Identity_Repo']
    issue_list_real = sorted([int(i) for i in issue_df.tolist()])
    if issue_list_real != issue_list:
        print(f'[{index + 1}] {repo_name}')
        print(f'Issue list recorded in repoDB: {len(issue_list)}-{issue_list}')
        print(f'Issue list recorded in issueDB: {len(issue_list_real)}-{issue_list_real}')