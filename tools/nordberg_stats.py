
from __future__ import print_function

import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from sqlalchemy import create_engine

engine   = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1/postgres')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

#credentials = service_account.Credentials.from_service_account_file('cred.json', scopes=SCOPES)

#spreadsheet_service = build('sheets', 'v4', credentials=credentials)

SAMPLE_SPREADSHEET_ID = '1h0GMdLtsxUUxqHf1C701hfY-XCGw78YGxtEJWZdHp-s'
SAMPLE_RANGE_NAME = 'Alltime!A2:AL26'

def main():
    #Credentials.from_authorized_user_file('cred.json', SCOPES)
    creds = service_account.Credentials.from_service_account_file('cred.json', scopes=SCOPES)



    try:
        '''sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        title = sheets[0].get("properties", {}).get("title", "Sheet1")
        sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)'''


        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        #sheet = service.spreadsheets()
        spreadsheet = service.spreadsheets()
        sheet_metadata = spreadsheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        #sheets = sheet.get('sheets',spreadsheetId=SAMPLE_SPREADSHEET_ID)
        for sheet in sheets:
            title = sheet['properties']['title']
            print(title)
            if len(title.split('-'))==2:
                season = f"20{title.split('-')[0]}-20{title.split('-')[1]}"
                result = spreadsheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                            range=f"'{title}'!C3:Y26").execute()
                values = result.get('values', [])

                columns= ['player', 'season', 'pts', 'trb', 'ast', 'stl', 'blk', 'ft', 'fta', '3p', 'pf', 'ft%', 'g','w','gs']
                #tot_columns= ['player', 'season', 'pts', 'trb', 'ast', 'stl', 'blk', 'ft', 'fta', '3p', 'pf', 'ft%', 'g','w','gs']

                avg_to_df = []
                tot_to_df = []
                for l in values:
                    player = l[0]
                    tot = l[1:14]


                    if int(l[11])>0:
                        ft = float(l[6])/int(l[11])
                        fta = float(l[7])/int(l[11])
                        ft_pct = 0 if fta==0 else ft/fta

                        avg = l[14:19] + [ft,
                                          fta,
                                          l[20],
                                          l[19],
                                          ft_pct,
                                          ] + l[11:14]

                        avg_to_df.append([player, season] + avg)
                        tot_to_df.append([player, season] + tot)

                df_avg = pd.DataFrame(avg_to_df,columns=columns)
                df_tot = pd.DataFrame(tot_to_df,columns=columns)

                df_avg.to_sql(name='player_pr_game',
                          con=engine,
                          schema='nor_stats',
                          if_exists='append')

                df_tot.to_sql(name='player_tot',
                              con=engine,
                              schema='nor_stats',
                              if_exists='append')

                #print(df_tot,df_avg)

            else:
                #alltime
                pass

                '''result = spreadsheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                  range=f"'{title}'!C3:AL26").execute()
                values = result.get('values', [])'''






        '''result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))'''
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()