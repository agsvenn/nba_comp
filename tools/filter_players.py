import pandas as pd

def filter_players_in_dataframe(df, conditions=[]):
    for condition in conditions:
        assert type(condition) is list and len(condition)==3, \
            'conditions must be passed as list with [col, criterion, value] \n    Not {}'
        assert condition[0] in df.columns, \
            f'column "{condition[0]}" not in columns. \n   Existing columns are {df.columns}'
        assert condition[1] in ['gr','ls','geq', 'leq', 'eql', 'isin', 'not','notin', 'cont'], \
            f"criterion '{condition[1]}' is not valid. \n   Must be in {['gr','ls','geq', 'leq', 'eql', 'isin', 'notin', 'cont']}"

        col = condition[0]
        c = condition[1]
        val = condition[2]

        if c == 'gr':
            df = df[df[col] > val]
        elif c == 'ls':
            df = df[df[col] < val]
        elif c == 'geq':
            df = df[df[col] >= val]
        elif c == 'leq':
            df = df[df[col] <= val]
        elif c == 'eql':
            df = df[df[col] == val]
        elif c == 'isin':
            assert type(val) is list, 'value must be list to pass isin'
            df = df[df[col].isin(val)]
        elif c == 'not':
            df = df[df[col] != val]
        elif c == 'notin':
            assert type(val) is list, 'value must be list to pass isin'
            df = df[~df[col].isin(val)]
        elif c == 'cont':
            #s = pd.Series([i.find(val) >= 0 for i in df[col]])
            #df =  df.where(s)
            #df = df[df[col].notna()]
            df = df[df[col].astype(str).str.contains(val)]
        else:
            pass

    return df