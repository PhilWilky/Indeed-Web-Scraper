import requests
from bs4 import BeautifulSoup
import pandas as pd
#ETL
#https://youtu.be/PPcgtx0sI2E


def extract(page):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    url = f'https://uk.indeed.com/jobs?q=junior+developer&l=Bingley&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for i in divs:
        title = i.find('a').text.strip()
        company = i.find('span', class_='company').text.strip()
        try:
            salary = i.find('span',
                            class_='salaryText').text.strip().replace('Â', '')
        except:
            salary = ''
        summary = i.find('div', class_='summary').text.strip().replace(
            '\n', '').replace('â€¦', '...')
        try:
            location = i.find('div', class_='location').text.strip()
        except:
            location = ''

        #Dictionary
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return


joblist = []

for i in range(0, 40, 10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')
print("finished...")
