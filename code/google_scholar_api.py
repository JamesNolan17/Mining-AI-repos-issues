import time
from urllib.error import HTTPError
import gscholar
from urllib.parse import quote
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

GOOGLE_SCHOLAR_URL = "https://scholar.google.com"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-SG,zh-CN;q=0.9,zh-Hans;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    'Cookie': "GSP=CF=%d" % 4
}
num = 1


def query(title_paper):
    global num
    title_paper_query = '/scholar?q=' + quote(title_paper)
    url = GOOGLE_SCHOLAR_URL + title_paper_query
    header = HEADERS
    header['Cookie'] = "GSP=CF=%d" % 4

    fetched = False
    while not fetched:
        try:
            request = Request(url, headers=header)
            response = urlopen(request)
            print(response.read())
            time.sleep(60)
            fetched = True
            soup = BeautifulSoup(response.read(), 'lxml')
            links = soup.find_all('a')
            for link in links:
                if link.text.startswith('Cited by '):
                    citation_number = int(link.text[8:])
                    print(f"{num}.{title_paper} - {citation_number}")
                    num += 1
                    return citation_number
        except Exception as e:
            print(f"{title_paper} - {e}")
            time.sleep(10)
            continue

    return -1


if __name__ == '__main__':
    df = pd.read_csv('repos.csv')
    df['Citation_Paper'] = df['Name_Paper'].apply(query)
    df.to_csv('paper_dataset.csv', index=False)
