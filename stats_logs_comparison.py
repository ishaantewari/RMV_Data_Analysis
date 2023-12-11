# UNFINISHED

import pandas as pd
from helpers import load_file
import matplotlib.pyplot as plt
import numpy as np

daily_stats = pd.read_csv('source_extract/daily_stats.csv')
daily_stats['Date'] = pd.to_datetime(daily_stats['Date'])


logs = load_file('cleaning_data/cleaned_logs.json')


dr = pd.date_range('2016-1-1', '2019-8-27')
lf = pd.DataFrame({'date': dr, 'logs': np.zeros(len(dr))})
lf.set_index(['date'], inplace=True)


for log in logs:
    lf.loc[f'{log["year"]}-{log["month"]}-{log["day"]}'] += 1


print(daily_stats[['local', 'state', 'federal']].sum(axis=1))



plt.plot(lf, label='logs')
plt.plot(daily_stats['Date'], daily_stats['multiples'], label='multiples')
plt.plot(daily_stats['Date'], daily_stats['local']+daily_stats['state']+daily_stats['federal'], label='local+state+fed')
plt.legend()
plt.show()
