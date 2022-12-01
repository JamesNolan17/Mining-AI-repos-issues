import pandas as pd
from github_token import *
import json
import time
start = time.time()

pwc = pd.read_csv('pwc.csv')
unique_conference = pwc["conference"].unique()
print(unique_conference)