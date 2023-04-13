from urllib.request import urlopen
import ssl
import json
import pandas as pd

#a = '[{"ttl":"Regular Season Averages","col":["season","Team",{"data":"GP","ttl":"Games Played"},{"data":"GS","ttl":"Games Started"},{"data":"MIN","ttl":"Minutes Per Game"},{"data":"FG","ttl":"Field Goals Made-Attempted Per Game"},{"data":"FG%","ttl":"Field Goal Percentage"},{"data":"3PT","ttl":"3-Point Field Goals Made-Attempted Per Game"},{"data":"3P%","ttl":"3-Point Field Goal Percentage"},{"data":"FT","ttl":"Free Throws Made-Attempted Per Game"},{"data":"FT%","ttl":"Free Throw Percentage"},{"data":"OR","ttl":"Offensive Rebounds Per Game"},{"data":"DR","ttl":"Defensive Rebounds Per Game"},{"data":"REB","ttl":"Rebounds Per Game"},{"data":"AST","ttl":"Assists Per Game"},{"data":"BLK","ttl":"Blocks Per Game"},{"data":"STL","ttl":"Steals Per Game"},{"data":"PF","ttl":"Fouls Per Game"},{"data":"TO","ttl":"Turnovers Per Game"},{"data":"PTS","ttl":"Points Per Game"}],"row":[["1996-97",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"76","74","40.1","8.2-19.8","41.6","2.0-6.0","34.1","5.0-7.2","70.2","1.5","2.6","4.1","7.5","0.3","2.1","3.1","4.4","23.5"],["1997-98",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"80","80","39.4","8.1-17.6","46.1","0.9-2.9","29.8","4.9-6.7","72.9","1.1","2.6","3.7","6.2","0.3","2.2","2.5","3.1","22.0"],["1998-99",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"48","48","41.5","9.1-22.0","41.2","1.2-4.1","29.1","7.4-9.9","75.1","1.4","3.5","4.9","4.6","0.1","2.3","2.0","3.5","26.8"],["1999-00",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"70","70","40.8","10.4-24.8","42.1","1.3-3.7","34.1","6.3-8.9","71.3","1.0","2.8","3.8","4.7","0.1","2.1","2.3","3.3","28.4"],["2000-01",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"71","71","42.0","10.7-25.5","42.0","1.4-4.3","32.0","8.2-10.1","81.4","0.7","3.1","3.8","4.6","0.3","2.5","2.1","3.3","31.1"],["2001-02",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"60","59","43.7","11.1-27.8","39.8","1.3-4.5","29.1","7.9-9.8","81.2","0.7","3.8","4.5","5.5","0.2","2.8","1.7","4.0","31.4"],["2002-03",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"82","82","42.5","9.8-23.7","41.4","1.0-3.7","27.7","7.0-9.0","77.4","0.8","3.4","4.2","5.5","0.2","2.7","1.8","3.5","27.6"],["2003-04",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"48","47","42.5","9.1-23.4","38.7","1.2-4.1","28.6","7.1-9.5","74.5","0.7","3.0","3.7","6.8","0.1","2.4","1.8","4.4","26.4"],["2004-05",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"75","75","42.3","10.3-24.2","42.4","1.4-4.5","30.8","8.7-10.5","83.5","0.7","3.3","4.0","7.9","0.1","2.4","1.9","4.6","30.7"],["2005-06",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"72","72","43.1","11.3-25.3","44.7","1.0-3.1","32.3","9.4-11.5","81.4","0.6","2.6","3.2","7.4","0.1","1.9","1.7","3.4","33.0"],["2006-07",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"15","15","42.7","10.1-24.4","41.3","0.8-3.5","22.6","10.3-11.6","88.5","0.5","2.3","2.7","7.3","0.1","2.2","1.4","4.4","31.2"],["2006-07",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"50","49","42.4","8.6-18.9","45.4","1.0-2.9","34.7","6.6-8.7","75.9","0.3","2.7","3.0","7.2","0.2","1.8","1.5","4.0","24.8"],["2007-08",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"82","82","41.8","8.7-19.0","45.8","1.2-3.4","34.5","7.9-9.7","80.9","0.6","2.4","3.0","7.1","0.1","2.0","1.3","3.0","26.4"],["2008-09",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"3","3","41.0","6.0-13.3","45.0","0.7-2.7","25.0","6.0-8.3","72.0","1.0","1.7","2.7","6.7","0.3","1.0","1.0","3.3","18.7"],["2008-09",{"name":"DET","uid":"s:40~l:46~t:8","component":"TeamLinks","href":"/nba/team/_/name/det/detroit-pistons","logo":"https://a.espncdn.com/i/teamlogos/nba/500/det.png"},"54","50","36.5","6.1-14.7","41.6","0.5-1.7","28.6","4.7-6.0","78.6","0.5","2.6","3.1","4.9","0.1","1.6","1.5","2.5","17.4"],["2009-10",{"name":"MEM","uid":"s:40~l:46~t:29","component":"TeamLinks","href":"/nba/team/_/name/mem/memphis-grizzlies","logo":"https://a.espncdn.com/i/teamlogos/nba/500/mem.png"},"3","0","22.3","5.0-8.7","57.7","0.3-0.3","100.0","2.0-4.0","50.0","0.3","1.0","1.3","3.7","0.0","0.3","1.7","2.3","12.3"],["2009-10",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"25","24","31.9","4.8-11.6","41.7","0.3-1.0","33.3","3.9-4.8","82.4","0.6","2.4","3.0","4.1","0.1","0.7","1.7","2.3","13.9"]],"car":["Career","","914","901","41.1","9.3-21.8","42.5","1.2-3.7","31.3","7.0-8.9","78.0","0.8","2.9","3.7","6.2","0.2","2.2","1.9","3.6","26.7"]},{"ttl":"Regular Season Totals","col":["season","Team",{"data":"FG","ttl":"Field Goals Made-Attempted"},{"data":"FG%","ttl":"Field Goal Percentage"},{"data":"3PT","ttl":"3-Point Field Goals Made-Attempted"},{"data":"3P%","ttl":"3-Point Field Goal Percentage"},{"data":"FT","ttl":"Free Throws Made-Attempted"},{"data":"FT%","ttl":"Free Throw Percentage"},{"data":"OR","ttl":"Offensive Rebounds"},{"data":"DR","ttl":"Defensive Rebounds"},{"data":"REB","ttl":"Rebounds"},{"data":"AST","ttl":"Assists"},{"data":"BLK","ttl":"Blocks"},{"data":"STL","ttl":"Steals"},{"data":"PF","ttl":"Fouls"},{"data":"TO","ttl":"Turnovers"},{"data":"PTS","ttl":"Points"}],"row":[["1996-97",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"625-1504","41.6","155-455","34.1","382-544","70.2","115","197","312","567","24","157","233","337","1787"],["1997-98",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"649-1407","46.1","70-235","29.8","390-535","72.9","86","210","296","494","25","176","200","244","1758"],["1998-99",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"435-1056","41.2","58-199","29.1","356-474","75.1","66","170","236","223","7","110","98","167","1284"],["1999-00",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"729-1733","42.1","89-261","34.1","442-620","71.3","71","196","267","328","5","144","162","230","1989"],["2000-01",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"762-1813","42.0","98-306","32.0","585-719","81.4","50","223","273","325","20","178","147","237","2207"],["2001-02",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"665-1669","39.8","78-268","29.1","475-585","81.2","44","225","269","331","13","168","102","237","1883"],["2002-03",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"804-1940","41.4","84-303","27.7","570-736","77.4","68","276","344","454","13","225","149","286","2262"],["2003-04",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"435-1125","38.7","57-199","28.6","339-455","74.5","34","144","178","324","5","115","87","209","1266"],["2004-05",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"771-1818","42.4","104-338","30.8","656-786","83.5","51","248","299","596","9","180","140","344","2302"],["2005-06",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"815-1822","44.7","72-223","32.3","675-829","81.4","44","188","232","532","10","140","121","248","2377"],["2006-07",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"151-366","41.3","12-53","22.6","154-174","88.5","7","34","41","109","1","33","21","66","468"],["2006-07",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"430-947","45.4","50-144","34.7","331-436","75.9","16","136","152","359","12","90","74","202","1241"],["2007-08",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"712-1556","45.8","95-275","34.5","645-797","80.9","47","196","243","586","12","160","109","245","2164"],["2008-09",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"18-40","45.0","2-8","25.0","18-25","72.0","3","5","8","20","1","3","3","10","56"],["2008-09",{"name":"DET","uid":"s:40~l:46~t:8","component":"TeamLinks","href":"/nba/team/_/name/det/detroit-pistons","logo":"https://a.espncdn.com/i/teamlogos/nba/500/det.png"},"330-794","41.6","26-91","28.6","253-322","78.6","27","138","165","263","5","85","83","136","939"],["2009-10",{"name":"MEM","uid":"s:40~l:46~t:29","component":"TeamLinks","href":"/nba/team/_/name/mem/memphis-grizzlies","logo":"https://a.espncdn.com/i/teamlogos/nba/500/mem.png"},"15-26","57.7","1-1","100.0","6-12","50.0","1","3","4","11","0","1","5","7","37"],["2009-10",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"121-290","41.7","8-24","33.3","98-119","82.4","15","60","75","102","2","18","43","57","348"]],"car":["Career","","8467-19906","42.5","1059-3383","31.3","6375-8168","78.0","745","2649","3394","5624","164","1983","1777","3262","24368"]},{"ttl":"Regular Season Misc Totals","col":["season","Team",{"data":"DD2","ttl":"Double Double"},{"data":"TD3","ttl":"Triple Double"},{"data":"DQ","ttl":"Disqualifications"},{"data":"EJECT","ttl":"Ejections"},{"data":"TECH","ttl":"Technical Fouls"},{"data":"FLAG","ttl":"Flagrant Fouls"},{"data":"AST/TO","ttl":"Assist To Turnover Ratio"},{"data":"STL/TO","ttl":"Steal To Turnover Ratio"},{"data":"RAT","ttl":"Rating"},{"data":"SC-EFF","ttl":"Scoring Efficiency"},{"data":"SH-EFF","ttl":"Shooting Efficiency"}],"row":[["1996-97",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"19","0","5","0","8","0","1.7","0.5","-","1.188","0.47"],["1997-98",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"12","0","2","0","14","0","2.0","0.7","-","1.249","0.49"],["1998-99",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"4","0","0","0","5","0","1.3","0.7","-","1.216","0.44"],["1999-00",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"1","0","1","0","12","0","1.4","0.6","-","1.148","0.45"],["2000-01",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"4","0","0","0","18","0","1.4","0.8","-","1.217","0.45"],["2001-02",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"4","1","0","1","12","0","1.4","0.7","-","1.128","0.42"],["2002-03",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"6","0","2","0","8","0","1.6","0.8","-","1.166","0.44"],["2003-04",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"8","0","0","0","7","0","1.6","0.6","-","1.125","0.41"],["2004-05",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"24","0","1","0","10","0","1.7","0.5","-","1.266","0.45"],["2005-06",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"18","0","0","0","13","0","2.1","0.6","-","1.305","0.47"],["2006-07",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"5","0","0","0","4","0","1.7","0.5","-","1.279","0.43"],["2006-07",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"12","0","0","1","8","0","1.8","0.4","-","1.310","0.48"],["2007-08",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"15","0","0","1","5","0","2.4","0.7","-","1.391","0.49"],["2008-09",{"name":"DEN","uid":"s:40~l:46~t:7","component":"TeamLinks","href":"/nba/team/_/name/den/denver-nuggets","logo":"https://a.espncdn.com/i/teamlogos/nba/500/den.png"},"0","0","0","0","1","0","2.0","0.3","-","1.400","0.48"],["2008-09",{"name":"DET","uid":"s:40~l:46~t:8","component":"TeamLinks","href":"/nba/team/_/name/det/detroit-pistons","logo":"https://a.espncdn.com/i/teamlogos/nba/500/det.png"},"2","0","0","0","4","0","1.9","0.6","-","1.183","0.43"],["2009-10",{"name":"MEM","uid":"s:40~l:46~t:29","component":"TeamLinks","href":"/nba/team/_/name/mem/memphis-grizzlies","logo":"https://a.espncdn.com/i/teamlogos/nba/500/mem.png"},"0","0","0","0","0","0","1.6","0.1","-","1.423","0.60"],["2009-10",{"name":"PHI","uid":"s:40~l:46~t:20","component":"TeamLinks","href":"/nba/team/_/name/phi/philadelphia-76ers","logo":"https://a.espncdn.com/i/teamlogos/nba/500/phi.png"},"0","0","0","0","1","0","1.8","0.3","-","1.200","0.43"]],"car":["Career","","134","1","11","3","130","0","1.7","0.6","-","1.224","0.45"]}]'

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

url = lambda year: f'https://www.espn.com/nba/stats/player/_/season/{year}/seasontype/2#'

page = urlopen(url(2001), context=context)

#page = urlopen('https://www.espn.com/nba/player/stats/_/id/366/allen-iverson', context=context)

html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)
print(len(html.split('https://www.espn.com/nba/player/_/id/')))

#print(json.loads(html.split('"tbl":')[1].split(',"gls":')[0]))