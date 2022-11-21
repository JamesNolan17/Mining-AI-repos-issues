import pandas as pd
from github_token import *
import time
repo_src = 'repoDB.csv'

df_repo = pd.read_csv(repo_src, encoding='latin-1')
for index, paper in df_repo.iterrows():
    df_issue = pd.DataFrame()
    print(f'[{index + 1}] {paper["Name_Repo"]}')
    repo_url = paper['Name_Repo']
    repo = g.get_repo(repo_url)
    contributors = repo.get_contributors()
    df_repo.loc[index, 'Contributors'] = "\n".join([_._identity for _ in contributors])
    print(df_repo.loc[index, 'Contributors'])
    df_repo.to_csv(repo_src, index=False)
