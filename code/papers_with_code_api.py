from github import Github
from paperswithcode import PapersWithCodeClient
import io, json
import pandas as pd
client = PapersWithCodeClient()
g = Github("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")
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
    "CHI"
]]
# conference_ids = ["aaai"]
paper_dataset = []
df = pd.DataFrame(columns=[
    "Name_Repo",
    "Name_Paper",
    "Conference_Paper",
    "Citation_Paper",
    "Num_Star",
    "Date_Created",
    "Date_Last_Mod",
    "Num_Issue",
    "IDList_Issue"
])
for conference_id in conference_ids:
    try:
        matched_conferences = client.proceeding_list(conference_id=conference_id)
        proceeding_ids = [conference.id for conference in matched_conferences.results]
        print(proceeding_ids)
        proceeding_ids.sort()
        # Build the paper dataset
        for proceeding_id in proceeding_ids:
                # paper_dataset[conference_id] = client.proceeding_paper_list(
                #    conference_id=conference_id,
                #    proceeding_id=proceeding_id)
                paper_dataset.extend(client.proceeding_paper_list(
                    conference_id=conference_id,
                    proceeding_id=proceeding_id).results)
    except Exception as e:
        print(f'{e}')
print(f'Number of papers: {len(paper_dataset)}')
repo_dataset = {}
for paper in paper_dataset:
    try:
        repo = client.paper_repository_list(paper_id=paper.id)
    except Exception as e:
        continue
    if repo.results:
        try:
            print(f'[{paper.title}] {repo.results[0].url}')
            name_repo = repo.results[0].url.replace('https://github.com/', '')
            name_paper = paper.title
            conference_paper = paper.proceeding
            citation_paper = -1
            num_star = repo.results[0].stars
            repo_g = g.get_repo(name_repo)
            date_created = repo_g.created_at
            date_last_mod = repo_g.updated_at
            num_issue = repo_g.get_issues().totalCount
            idlist_issue = -1
            repo_dataset[paper.title] = repo.results[0].url
            df = df.append({"Name_Repo": name_repo, "Name_Paper": name_paper, "Conference_Paper": conference_paper,
                            "Citation_Paper": citation_paper, "Num_Star": num_star, "Date_Created": date_created,
                            "Date_Last_Mod": date_last_mod, "Num_Issue": num_issue, "IDList_Issue": idlist_issue},
                           ignore_index=True)
            df.to_csv('repos.csv', index=False)
        except Exception as e:
            print(f'{e}')
            continue
print(f'Number of repos: {len(repo_dataset.keys())}')
with io.open('repos.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(repo_dataset, ensure_ascii=False))