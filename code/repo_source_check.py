import pandas as pd
import os


def repo_source_check():
    repo_input_name = 'repoDB_RAW.csv'
    repo_db = pd.read_csv(repo_input_name)
    print(f"Total number of repos: {len(repo_db)}")

    repo_src = {}


    for index, row in repo_db.iterrows():
        url = row['Name_Repo']
        url_split = url.split('/')
        if url_split[2] in repo_src:
            repo_src[url_split[2]] += 1
        else:
            repo_src[url_split[2]] = 1
    # print the percentage of repo_src
    for key in repo_src:
        print(f'{key}: {repo_src[key]/len(repo_db)*100:.2f}%')
    print(repo_src)
    print(f"Total number of repo sources: {len(repo_src)}")

if __name__ == '__main__':
    repo_source_check()
