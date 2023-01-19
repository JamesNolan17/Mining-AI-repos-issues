# Mine GitHub Issues
## The database:
There are 2 databases that are used in this project: 
1. `repoDB.csv`: Contains all repositories that are mined by PapersWithCode API under the following contains:  `conference_ids = [_.lower() for _ in ["CVPR","ICLR","ICML","NeurIPS","ECCV","ICCV","AAAI","ACL","SIGKDD","AAMAS"]]`

| Column Name                  | Description                                                                                                                                                                                                                      | Fetched From     |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| Name_Repo                    | The name of the repository. ```creator_name/repo_name```, which can be used to fetch the information of that repository.                                                                                                         | Papers With Code |
| Name_Paper                   | The name of the paper corresponding to the repository.                                                                                                                                                                           | Papers With Code |
| Conference_Paper             | The conference of the paper being published.                                                                                                                                                                                     | Papers With Code |
| Year_Paper                   | The year of the paper being published.                                                                                                                                                                                           | Papers With Code |
| URL_Repo                     | The URL of the repo.                                                                                                                                                                                                             | Papers With Code |
| URL_Paper                    | The URL of the paper.                                                                                                                                                                                                            | Papers With Code |
| Framework                    | The major framework used in the repo.                                                                                                                                                                                            | Papers With Code |
| Owners                       | The owner type of the repo, academia or industry.                                                                                                                                                                                | Self Annotated   |
| Mono_Repo                    | Whether the repo is a mono repo.                                                                                                                                                                                                 | Self Annotated   |
| Issue_Types                  | The Type of issues that are set in this repository. Usually if the maintainer didn't create new issue types, there are still default issue types automatically generated by GitHub. Seperated by `#`                             | PyGitHub         |
| IDList_Issue                 | The list of IDs of all the issues (Both open and closed) obtained, seperated by ```#```. For example, ```2#1``` means that there are 2 issues in total, ```1``` and ```2```. This field will be blank if no issues are proposed. | PyGitHub         |
| Num_Star                     | The number of star this repository got so far.                                                                                                                                                                                   | PyGitHub         |
| Num_Fork                     | The number of fork this repository got so far.                                                                                                                                                                                   | PyGitHub         |
| Num_Watcher                  | The number of wather this repository got so far.                                                                                                                                                                                 | PyGitHub         |
| Date_Created                 | The date when this repository was created.                                                                                                                                                                                       | PyGitHub         |
| Date_Last_Mod                | The date when this repository was last modified.                                                                                                                                                                                 | PyGitHub         |
| Num_Issue                    | Number of issues this repository obtained so far. **Num_Issue = Num_Issue_Open + Num_Issue_Closed**                                                                                                                              | PyGitHub         |
| Num_Issue_Type               | The number of issue types set in this repository.                                                                                                                                                                                | PyGitHub         |
| Num_Issue_Open               | Number of issues in this repository which are still open.                                                                                                                                                                        | PyGitHub         |
| Num_Issue_Closed             | Number of issues in this repository which are closed.                                                                                                                                                                            | PyGitHub         |
| Contributors                 | The name of contributors of this repository, seperated by `\n`. These names can be used to query the user's metadata.                                                                                                            | PyGitHub         |
| Num_Issue_Open_No_Assignee   | The number of open issues in this reposity with no assignee.                                                                                                                                                                     | PyGitHub         |
| Num_Issue_Open_No_Label      | The number of open issues in this reposity with no label.                                                                                                                                                                        | PyGitHub         |
| Num_Issue_Closed_No_Assignee | The number of closed issues in this reposity with no assignee.                                                                                                                                                                   | PyGitHub         |
| Num_Issue_Closed_No_Label    | The number of closed issues in this reposity with no label.                                                                                                                                                                      | PyGitHub         |
| Num_Issue_Type_Unused        | The number of issue types that are totally unused so far. (Unused by both open issues and closed issues)                                                                                                                         | PyGitHub         |



2. `issueDB.csv`: For every repository in `repoDB.csv`, we fetched all issues (both open issues and closed issues) under it. The mapping relationship between `issueDB.csv` and `repoDB.csv` are:

   **issue i in repo r** : `i[Name_Repo] == r[Name_Repo] & i[Identity_Repo] in r[IDList_Issue]`

   A cross check between these 2 DBs are conducted to ensure the integrity of them.

| Column Name     | Description                                                                                         | Fetched From |
|-----------------|-----------------------------------------------------------------------------------------------------|--------------|
| Title           | The issue title.                                                                                    | PyGitHub     |
| Name_Repo       | The repository that this issue belongs to.                                                          | PyGitHub     |
| State           | Whether this issue is currently open or closed. The value is either `open` or `closed`.             | PyGitHub     |
| Assignees       | The assignee of this issue. Empty means no assignee.                                                | PyGitHub     |
| Proposed_By     | The name of GitHub user who proposed the issue.                                                     | PyGitHub     |
| Closed_By       | The name of GitHub user who closed the issue.                                                       | PyGitHub     |
| Date_Created    | The date when this issue was created.                                                               | PyGitHub     |
| Date_Closed     | The date when this issue was closed. Empty for open issues.                                         | PyGitHub     |
| Num_Comment     | Number of comment this issue got so far (for open issues)/before it is resolved(for closed issues). | PyGitHub     |
| Label_Issue     | The labels of this issue, seperated by `#`.                                                         | PyGitHub     |
| Identity_Repo   | The id of this issue within the repo.                                                               | PyGitHub     |
| Identity_Global | The id of this issue in GitHub.                                                                     | PyGitHub     |
| Body            | The content of this issue.                                                                          | PyGitHub     |
| Sentiment_Title | The sentiment result of this issue's title.                                                         | Senti4SD     |
| Sentiment_Body  | The sentiment result of this issue's body.                                                          | Senti4SD     |
