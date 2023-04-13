from urllib.request import urlopen
from urllib.error import HTTPError
import ssl
import json
import pandas as pd
import time
import psycopg2
from sqlalchemy import create_engine
from tqdm import tqdm


# Create an engine instance
def get_last_id():
    conn = psycopg2.connect(database='postgres',
                            user='postgres',
                            password='postgres',
                            host='127.0.0.1',
                            port=5432)
    cur = conn.cursor()
    cur.execute('select max(id) from nba_stats.average')
    last_id = cur.fetchall()[0][0]
    conn.close()

    return last_id


resume_id = get_last_id()
engine   = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1/postgres')

def vask(stats_str):#, player_url):
    di = json.loads(stats_str)

    ut_di = {}

    for i in di:
        table_name = i['ttl']
        columns = []
        for col in i['col']:
            if type(col) == str:
                columns.append(col)
            else:
                if col['data'] in ['FG', '3PT', 'FT']:
                    columns.append(col['data']+'_MADE')
                    columns.append(col['data']+'_ATTEMPTS')
                else:
                    columns.append(col['data'])

        stats  = []

        for row in i['row']:
            rows = [row[0], row[1]['name']]

            for c in row[2:]:
                if len(c.split('-')) == 2 and len(c)==1:
                    rows.append('-')
                elif len(c.split('-')) == 2:
                    m, a = c.split('-')
                    rows.append(float(m))
                    rows.append(float(a))
                else:
                    rows.append(float(c))
            stats.append(rows)

        career = [i['car'][0], i['car'][1]]
        for c in i['car'][2:]:
            if len(c.split('-')) == 2 and len(c)==1:
                career.append('-')
            elif len(c.split('-')) == 2:
                m, a = c.split('-')
                career.append(float(m))
                career.append(float(a))
            else:
                career.append(float(c))
        stats.append(career)

        #print(career)
        ut_di[table_name] = pd.DataFrame(stats, columns=columns)

    return ut_di




# This restores the same behavior as before.
context = ssl._create_unverified_context()

url = lambda id: f'https://www.espn.com/nba/player/stats/_/id/{id}'

for id in tqdm(range(resume_id+1,11000+resume_id)):
    try:
        page = urlopen(url(id), context=context)

        #page = urlopen('https://www.espn.com/nba/player/stats/_/id/366/allen-iverson', context=context)

        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        player_name = html.split(f'/nba/player/advancedstats/_/id/{id}/',1)[1].split('"')[0]
        try:
            dfs = vask(html.split('"tbl":')[1].split(',"gls":')[0])

            df_misc = dfs['Regular Season Misc Totals']
            df_totals = dfs['Regular Season Totals']
            df_avg = dfs['Regular Season Averages']



            for df,name in zip([df_misc,df_totals,df_avg], ['misc','totals','average']):
                df['id'] = id
                df['player_name'] = player_name
                #print(player_name,end='\r')
                df.to_sql(name=name,
                          con=engine,
                          schema='nba_stats',
                          if_exists='append')
        except KeyError:
            pass

        #df.to_sql(name=)
    except HTTPError:
        pass

    #time.sleep(1)
