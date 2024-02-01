import sys
sys.path.append('../NewtonHS_RMV_emails')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from helpers import load_file




# CHOOSE WHICH COLUMNS TO PLOT ON GRAPH HERE
COLS_TO_PLOT = ['logs', 'fr_reqs', 'loc+state+fed']




daily_stats = pd.read_csv('data/source_extract/daily_stats.csv')
daily_stats['Date'] = pd.to_datetime(daily_stats['Date'])


logs = load_file('data/other_data/cleaned_logs_with_non_emails.json')

dr = pd.date_range('2016-1-1', '2019-8-27')
lf = pd.DataFrame({'date': dr, 'logs': np.zeros(len(dr))})
lf.set_index(['date'], inplace=True)


for log in logs:
    lf.loc[f'{log["year"]}-{log["month"]}-{log["day"]}'] += 1


# chop off the tail of stats, where the data is iffy
daily_stats = daily_stats[daily_stats['Date'] <= '2019-07-01']
daily_stats.set_index(['Date'], inplace=True)

# combine all data!! :D
df = pd.merge(lf, daily_stats, how='outer', left_index=True, right_index=True)
df.index.name = 'date'

# chop off beginning and end of df, where data is iffy
df = df[df.index >= '2016-09-01']
df = df[df.index <= '2019-05-31']

# sum local, state, and federal columns
df['loc+state+fed'] = df['local'] + df['state'] + df['federal']


# define a function that makes graphing easier
def plot_cols(cols, group_by: str):

    print("")

    if group_by == "month" :
        freq = 'M'
    elif group_by == 'week':
        freq = 'W'
    else:
        freq = 'D'
    
    for col in cols:

        # "smooth" the graph
        grouped_col = df.groupby(pd.Grouper(level='date', freq=freq))[col].sum()
        grouped_logs = df.groupby(pd.Grouper(level='date', freq=freq))['logs'].sum()
        print(col, ".......", "total: ", df[col].sum(), "... corr ind: ", round(np.corrcoef(grouped_logs, grouped_col)[0,1], 3))
        
        plt.plot(grouped_col, label=col)

# graph the logs in comparison to other columns to find out which one most closely resembles the logs
plot_cols(['logs', 'fr_reqs', 'loc+state+fed'], group_by="month")

plt.legend()
plt.show()