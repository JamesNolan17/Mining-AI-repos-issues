from github import Github
import pandas as pd

g = Github("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")
repo_input_name = 'repoDB_RM_MTO.csv'
repo_output_name = 'repoDB_RM_NON_GH.csv'
repo_db = pd.read_csv(repo_input_name)
prefix = 'https://github.com/'
for index, row in repo_db.iterrows():
    if not row['Name_Repo'].startswith(prefix):
        repo_db = repo_db.drop(index)

for index, row in repo_db.iterrows():
    repo_db.loc[index, 'Name_Repo'] = row['Name_Repo'][len(prefix):]

repo_db.to_csv(repo_output_name, index=False)
print(f'Number of rows: {len(repo_db)}')