import pandas as pd
import numpy as np

df_repo = pd.read_csv('repoDB.csv')
df_issue = pd.read_csv('issueDB.csv')
for index, paper in df_repo.iterrows():
    #print(f'[{index + 1}] {paper["Name_Repo"]}')
    repo_name = paper['Name_Repo']
    issue_string = str(paper['IDList_Issue'])
    if issue_string == 'nan':
        issue_list = []
    else:
        issue_list = [int(i) for i in issue_string.split('#')]
    #print(issue_list)
    issue_df = df_issue.query(f"`Name_Repo` == '{repo_name}'")['Identity_Repo']
    issue_list_real = issue_df.tolist()
    if issue_list_real != issue_list:
        print(repo_name)
        print(f'Issue list recorded in repoDB: {len(issue_list)}-{issue_list}')
        print(f'Issue list recorded in issueDB: {len(issue_list_real)}-{issue_list_real}')
        if repo_name == "khetan2/MBEM":
            df_issue.query(f"`Name_Repo` == '{repo_name}'").to_csv('issue51.csv')