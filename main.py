import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np
import warnings
from tools.filter_players import filter_players_in_dataframe
from tools.avstand import avstand_beregn
import uuid
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 500)

alchemyEngine   = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1', pool_recycle=3600)
dbConnection    = alchemyEngine.connect()

df_stats = pd.read_sql(text('''select player, season,tm, g, gs, pts, trb, ast, stl, blk, pf, "3p" 
                                 from nba_stats_br.player_pr_game'''), con=dbConnection)
df_blag = pd.read_sql(text('''select player, season, 'NOR' as tm, g, gs, pts, trb, ast, stl, blk, pf, "3p" 
                                 from nor_stats.player_pr_game order by player, season'''),con=dbConnection)

#df_blag = pd.read_sql(text('''select player, 'alltime', 'NOR', g, gs, pts, trb, ast, stl, blk, pf, "3p" from nor_stats.player_career_avg'''),con=dbConnection)


columns = ['player', 'season','tm', 'g', 'gs', 'pts', 'trb', 'ast', 'stl', 'blk', 'pf', '3p']

c_sammenlign = ['pts', 'trb', 'ast', 'stl', 'blk', 'pf', '3p']

nba_mean = [df_stats[col].mean() for col in c_sammenlign]
nba_median = [df_stats[col].median() for col in c_sammenlign]
nba_max = [df_stats[col].max() for col in c_sammenlign]
nba_std = [df_stats[col].std() for col in c_sammenlign]

nor_mean = [df_blag[col].mean() for col in c_sammenlign]
nor_max = [df_blag[col].max() for col in c_sammenlign]
nor_std = [df_blag[col].std() for col in c_sammenlign]

felles_mean = [np.array([i,j]).mean() for i,j in zip(nba_mean,nor_mean)]
felles_max = [np.array([i,j]).max() for i,j in zip(nba_max,nor_max)]
vekting = [i/(j*1.2) for i,j in zip(nba_mean,nor_mean)]

#print(1/np.array(vekting))
nba_sesonger = ['2009-2010',
                '2010-2011',
                '2011-2012',
                '2013-2014',
                '2015-2016',
                '2016-2017',
                '2017-2018',
                '2018-2019',
                '2019-2020',
                '2020-2021',
                '2021-2022',
                '2022-2023']

df_stats = filter_players_in_dataframe(df_stats,[ ['g','gr',20]])#,#])#,
                                                  #['player','cont','\*']
                                                  #['season','isin',nba_sesonger]
                                                  #])
df_blag = filter_players_in_dataframe(df_blag)#,[#['player','eql','L. Gjesvik'],
                                               #['season','notin', ['2021-2022','2016-2017'] ],
                                               # ['season', 'eql', '2018-2019']])

assert len(df_blag)>0, 'sjekk kriterier for blags filter. Null rader spyttet ut'
assert len(df_stats)>0, 'sjekk kriterier for nba filter. Null rader spyttet ut'

df_comp_stats = df_stats[c_sammenlign]
df_comp_blag = df_blag[c_sammenlign]

a = avstand_beregn(nba_max,nba_mean,nor_max,nor_mean,c_sammenlign)
doc_id = 0

for i in range(len(df_blag)):
    l = []
    mc = -1000

    nor = np.array(df_comp_blag.iloc[i])
    # nor_ = nor/np.array(nor_max)
    # nor_ = nor/np.array(nba_max)
    nor_ = nor/np.array(felles_max)*1.2

    a.init_nordberg(nor_, vekting,felles_max,felles_mean)

    for j in range(len(df_stats)):
        nba = np.array(df_comp_stats.iloc[j])
        # nba_ = nba/np.array(nba_max)
        nba_ = nba/np.array(felles_max)

        a.init_nba(nba_)

        # corr = a.pearsonish()
        # corr = a.numpy_corr()
        # corr = a.scipy_corr()
        # corr = a.scipy_corr('spearman')
        # corr = a.scipy_corr('kendall')
        corr = a.diff()

        if corr > mc:

            mc = corr
            l.append(list(df_stats.iloc[j])+[float(corr)])

    l.append(list(df_blag.iloc[i])+[mc+1])
    compdf = pd.DataFrame(l,columns=columns+['corr'])
    compdf = compdf.sort_values(by='corr',ascending=False)[:min([len(compdf),5])]
    print(compdf)
    compdf.to_latex(f'latex/tables/a_{doc_id}.tex')
    doc_id+=1

    print('-----------------------------------------------')



