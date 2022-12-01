from github import Github
from paperswithcode import PapersWithCodeClient
import io, json
import pandas as pd

client = PapersWithCodeClient()
g = Github("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")
repo_name = 'repoDB_RAW.csv'
repo_db = pd.read_csv(repo_name)

# Constrain 1: Conference List
conference_ids = [_.lower() for _ in [
    "CVPR",
    "ICLR",
    "ICML",
    "NeurIPS",
    "ECCV",
    "ICCV",
    "AAAI",
    "ACL",
    "SIGKDD",
    "AAMAS"
]]

# Constrain 2: Year Limit
year_limit = [2012,2022]

paper_list = []
for conference_id in conference_ids:
    try:
        matched_conferences = client.proceeding_list(conference_id=conference_id)
        for proceeding_metadata in matched_conferences.results:
            year = proceeding_metadata.year
            # Constrain 2: Year Limit
            if year < year_limit[0] or year > year_limit[1]:
                continue
            paper_list.extend(
                client.proceeding_paper_list(conference_id=conference_id,
                                             proceeding_id=proceeding_metadata.id).results)
    except Exception as e:
        print(f'{conference_id}-{e}')
print(f'Number of papers: {len(paper_list)}')
repo_dataset = {}

for paper in paper_list:
    try:
        repo = client.paper_repository_list(paper_id=paper.id)
    except Exception as e:
        continue
    if repo.results:
        try:
            print(f'[{paper.title}] {repo.results}')
            print(len(repo.results))
            for result in repo.results:
                # Constrain 3: Official Implementation
                if not result.is_official: continue
                name_repo = result.url
                name_paper = paper.title
                conference_paper, year = paper.proceeding.split("-")[:2]
                framework = result.framework
                repo_db = repo_db.append(
                    {'Name_Repo': name_repo,
                     'Name_Paper': name_paper,
                     'Conference_Paper': conference_paper,
                     'URL_Repo': result.url,
                     'URL_Paper': paper.url_pdf,
                     'Year_Paper': year,
                     'Framework': framework
                     }, ignore_index=True)
                repo_db.to_csv(repo_name, index=False)
        except Exception as e:
            print(f'{e}')
            continue

print(f'Number of repos: {len(repo_db)}')
