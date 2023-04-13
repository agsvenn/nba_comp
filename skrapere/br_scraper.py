import time
from urllib.request import urlopen
import ssl
import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from sqlalchemy import create_engine

engine   = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1/postgres')

# This restores the same behavior as before.
context = ssl._create_unverified_context()

url_avg = lambda year: f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'
url_tot = lambda year: f'https://www.basketball-reference.com/leagues/NBA_{year}_totals.html'

def ids(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    table1 = soup.find('table', id='per_game_stats')
    table1.find_all()
    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)
    print(headers)

    #html_str.split('href="/players/a/'

def average(year_start,year_end):

    for y in tqdm(range(year_start,year_end)):
        page = urlopen(url_avg(y), context=context)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        dfs = pd.read_html(io=html,
                        extract_links='body')

        if len(dfs)>1:
            print(dfs)
            input()
        else:
            df = dfs[0]

            s_pid = df['Player'].apply(pd.Series)[1]
            df = df.applymap(lambda x: x[0])
            df['player_id'] = s_pid
            df.columns = [col.lower() for col in df.columns]

            df['season'] = f'{y-1}-{y}'
            df = df[df.gs != 'GS'].replace("",0)

            #df = df.applymap(lambda x: x.replace("", 0))
            #df = df.convert_dtypes().dtypes

            df.to_sql(name='player_pr_game',
                      con=engine,
                      schema='nba_stats_br',
                      if_exists='append')
        time.sleep(5)

def totals(year_start,year_end):

    for y in tqdm(range(year_start,year_end)):
        page = urlopen(url_tot(y), context=context)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        dfs = pd.read_html(io=html,
                           extract_links='body')
        if len(dfs)>1:
            print(dfs)
            input()
        else:
            df = dfs[0]

            s_pid = df['Player'].apply(pd.Series)[1]
            df = df.applymap(lambda x: x[0])
            df['player_id'] = s_pid
            df.columns = [col.lower() for col in df.columns]

            df['season'] = f'{y-1}-{y}'
            df = df[df.gs != 'GS'].replace("",0)

            #df = df.convert_dtypes().dtypes

            df.to_sql(name='player_total',
                          con=engine,
                          schema='nba_stats_br',
                          if_exists='append')
        time.sleep(5)


average(2023,2024)
totals(2023,2024)
'''
soup = BeautifulSoup(html, 'lxml')


table1 = soup.find('table', id='per_game_stats')
table1.find_all()
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
print(headers)
#print(len(html.split('https://www.espn.com/nba/player/_/id/')))

#print(json.loads(html.split('"tbl":')[1].split(',"gls":')[0]))
'''