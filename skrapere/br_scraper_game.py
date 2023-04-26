import time
from urllib.request import urlopen
import ssl
import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from sqlalchemy import create_engine
import numpy as np

engine   = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1/postgres')

# This restores the same behavior as before.
context = ssl._create_unverified_context()

url_gme = lambda year, month: f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html'

months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may']

def vask(df, id_col, id_col_ut, filter_column, filter_value, y):
    gid = df[id_col].apply(pd.Series)[1]

    df = df.applymap(lambda x: x[0])
    df[id_col_ut] = gid
    df.columns = [col.lower() for col in df.columns]

    df['season'] = f'{y-1}-{y}'
    df = df[df[filter_column] != filter_value].replace("",0).replace('Did Not Play', np.nan)

    return df

def game(year_start,year_end):
    ts = 3.2
    for y in range(year_start,year_end):

        for m in months:
            print(m, y, ':')
            time.sleep(ts)
            page = urlopen(url_gme(y, m), context=context)

            html_bytes = page.read()
            html = html_bytes.decode("utf-8")

            dfs = pd.read_html(io=html,
                            extract_links='body')
            df = dfs[0]
            #print(dfs)
            if 'Unnamed: 5' in df.columns:
                gid = df['Unnamed: 5'].apply(pd.Series)[1]
            else:
                gid = df['Unnamed: 6'].apply(pd.Series)[1]

            df = df.applymap(lambda x: x[0])
            df['game_id'] = gid
            df.columns = [col.lower().split('/')[0] for col in df.columns]

            df['season'] = f'{y-1}-{y}'
            df = df[df.date != 'DATE']
            df = df[['game_id','season','date','visitor', 'pts', 'home', 'pts.1','attend.', 'arena']]
            df.columns = ['game_id', 'season', 'date','visitor', 'pts_v', 'home', 'pts_h','attendance', 'arena']

            df.to_sql(name='games',
                      con=engine,
                      schema='nba_stats_br',
                      if_exists='append')

            for gid, v, h in zip(df.game_id, df.visitor, tqdm(df.home)):
                time.sleep(ts)
                game_url = 'https://www.basketball-reference.com' + gid

                page = urlopen(game_url,context=context)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")

                dfs = pd.read_html(io=html,
                               extract_links='body')

                dfs_basic = []
                for i in range(len(dfs)):
                    if 'Basic Box Score Stats' in dfs[i].columns.get_level_values(0):
                        dfs_basic.append(dfs[i])

                df_v = dfs_basic[0]
                df_h = dfs_basic[int(len(dfs_basic)/2)]
                df_v.columns = [col[1] for col in df_v.columns]
                df_h.columns = [col[1] for col in df_h.columns]



                df_v = vask(df_v[df_v.Starters!='Team Totals'],'Starters', 'player_id', 'mp', 'MP',y)
                df_h = vask(df_h[df_h.Starters!='Team Totals'],'Starters', 'player_id', 'mp', 'MP',y)
                df_v['team'], df_v['game_id'] = v, gid
                df_h['team'], df_h['game_id'] = h, gid

                pd.concat([df_v,df_h]).to_sql(name='player_game',
                          con=engine,
                          schema='nba_stats_br',
                          if_exists='append')



            input()





game(1980,1981)

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