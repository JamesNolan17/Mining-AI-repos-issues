import pandas as pd

repo_input_name = 'repoDB_RAW.csv'
repo_output_name = 'repoDB.csv'
repo_db = pd.read_csv(repo_input_name)
print(f"Total number of repos: {len(repo_db)}")

# Remove unofficial implementation
for index, row in repo_db.iterrows():
    if row['Official_Implementation'] != 1:
        repo_db = repo_db[repo_db.Name_Repo != row['Name_Repo']]
print("Unofficial implementation removed!")

# Detect MTO and OTM (By right there should be no MTO and OTM)
paper_set = set()
repo_set = set()

for index, row in repo_db.iterrows():
    if row['Name_Paper'] in paper_set:
        print(f'Paper {row["Name_Paper"]} already exists')
    paper_set.add(row['Name_Paper'])

for index, row in repo_db.iterrows():
    if row['Name_Repo'] in repo_set:
        print(f'Repo {row["Name_Repo"]} already exists')
    repo_set.add(row['Name_Repo'])

# Check non-GH repo + shorten repo name
prefix = 'https://github.com/'
for index, row in repo_db.iterrows():
    if not row['Name_Repo'].startswith(prefix):
        repo_db = repo_db.drop(index)
        print(f'Repo {row["Name_Repo"]} is not a GitHub repo, dropped.')

for index, row in repo_db.iterrows():
    repo_db.loc[index, 'Name_Repo'] = row['Name_Repo'][len(prefix):]

for index, row in repo_db.iterrows():
    if len(row['Name_Repo'].split('/')) != 2:
        print(f'Nested repo: {row["Name_Repo"]}')
        #repo_db = repo_db.drop(index)

# Drop the Official_Implementation column
repo_db = repo_db.drop(columns=['Official_Implementation'])
repo_db.to_csv(repo_output_name, index=False)
print(f"Total number of repos: {len(repo_db)}")
