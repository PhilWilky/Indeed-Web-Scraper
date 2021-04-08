import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#ETL


# EXTRACT
def extract(page):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    url = f'https://uk.indeed.com/jobs?q=Junior+Developer&l=Bingley&radius=10&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


# TRANSFORM
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


# LOAD
joblist = []

for i in range(0, 80, 10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
#work out the current path
full_path = os.path.realpath(__file__)
cwd = os.path.dirname(full_path)
#Create ouput inside current path
path = cwd + "/jobs.csv"
df.to_csv(path, encoding='utf-8-sig')
#Report as finished
print("finished...")
