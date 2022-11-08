import pandas as pd
from github import Github
import json
import time
start = time.time()
g = Github("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")
#g = Github("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")

while True:
    print(g.get_rate_limit().core.remaining)