from github import Github
from paperswithcode import PapersWithCodeClient
import io, json
import pandas as pd

g = Github("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")
repo_input_name = 'repoDB_RAW.csv'
repo_output_name = 'repoDB_RM_MTO.csv'
repo_db = pd.read_csv(repo_input_name)
print(f"Total number of repos: {len(repo_db)}")

paper_set = set()
repo_set = set()

for index, row in repo_db.iterrows():
    if row['Name_Paper'] in paper_set:
        print(f'Paper {row["Name_Paper"]} already exists')
        repo_db = repo_db[repo_db.Name_Paper != row['Name_Paper']]
        continue
    paper_set.add(row['Name_Paper'])

for index, row in repo_db.iterrows():
    if row['Name_Repo'] in repo_set:
        print(f'Repo {row["Name_Repo"]} already exists')
        repo_db = repo_db[repo_db.Name_Repo != row['Name_Repo']]
        continue
    repo_set.add(row['Name_Repo'])

repo_db.to_csv(repo_output_name, index=False)
print(f'Number of papers: {len(paper_set)}')
print(f'Number of rows: {len(repo_db)}')