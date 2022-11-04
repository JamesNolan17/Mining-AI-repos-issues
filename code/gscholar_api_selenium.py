import copy
import json
import time
import urllib.request
from random import random, randint
from urllib.parse import quote

import pandas as pd
from selenium import webdriver
import requests
import re
import time

from selenium.webdriver.common.by import By

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-SG,zh-CN;q=0.9,zh-Hans;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    'Cookie': "GSP=CF=%d" % 4
}


PATH = "./chromedriver"
GOOGLE_SCHOLAR_URL = "https://scholar.google.com"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"

# HEADLESS
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--user-agent=%s' % user_agent)
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=PATH, options=options)
driver.set_window_size(700, 800)
num = 539
def get_citation(name_paper):
    global num
    # Example for 0 citation
    # name_paper = "Learning ABCs: Approximate Bijective Correspondence for isolating factors of variation with weak supervision"
    dst_url = GOOGLE_SCHOLAR_URL + '/scholar?hl=en&as_sdt=0%2C5&q=' + quote(name_paper)
    driver.get("https://scholar.google.com")
    driver.add_cookie({'name': 'GSP', 'value': 'LM=1664867209:S=qKd-exHzbn1xklcN'})
    driver.get(dst_url)
    a_tags = driver.find_elements(By.XPATH, "//a[@href]")
    robot_tags = driver.find_elements(By.XPATH, "//h1")
    if robot_tags:
        for robot_tag in robot_tags:
            if robot_tag.text == "Please show you're not a robot":
                print("Robot detected")
                driver.quit()
                exit(0)

    for a in a_tags:
        if a.text == "Related articles":
            print(f"{num}.{name_paper} - NOT CITED")
            num += 1
            return 0
        if a.text.startswith("Cited by "):
            print(f"{num}.{name_paper} - {a.text[8:]}")
            num += 1
            time.sleep(randint(5, 10))
            return int(a.text[8:])
    return -999

if __name__ == '__main__':
    df = pd.read_csv('repos.csv')
    num_paper = num
    for index, row in df.iterrows():
        if index < num_paper - 2:
            continue
        df.loc[index, 'Citation_Paper'] = get_citation(row['Name_Paper'])
        df.to_csv('repos.csv', index=False)