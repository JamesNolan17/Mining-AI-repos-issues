import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


repo_db = pd.read_csv('repo_db.csv')
star_distribution = repo_db['Num_Star'].value_counts()
fork_distribution = repo_db['Num_Fork'].value_counts()

sorted_star_distribution = star_distribution.sort_index()
