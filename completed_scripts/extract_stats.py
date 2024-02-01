import pandas as pd
import glob
import numpy as np
import re


# [1] EXTRACT DATA

path = r'data/docs_source/stats'
all_stats_files = glob.glob(path + "/*.xlsx")

# extract each spreadsheet into an array of worksheets
# each worksheet contains one week's worth of data

months = []
month_sums = []

for filename in all_stats_files:
    
    xls = pd.ExcelFile(filename)

    weeks = []

    for sheet_name in xls.sheet_names:
        weeks.append(xls.parse(sheet_name))


    # the last df in the weeks array is the monthly summary
    month_sum = weeks.pop(-1)


    # PROCESS DAILY SUMMARIES
    # remove the last row of each week, which represents the sum of all the data
    for week in weeks:
            week.drop(week.tail(1).index, inplace=True)

    # concatenate the weeks into one df that represnts a month
    month = pd.concat(weeks, axis=0, ignore_index=True)

    # include the filename
    month['Root File'] = filename


    # PROCESS MONTHLY SUMMARY

    # find the date from the filename

    date_string = re.search('s/(.*) Fa', filename)[0][2:-3]
    date = pd.to_datetime(date_string)

    # flip the file around so that the axes are properly aligned!
    # and make the indeces the dates
    month_sum = month_sum.transpose()
    month_sum = pd.DataFrame(month_sum.values[1:], columns=month_sum.iloc[0])
    month_sum.set_index([pd.Index([date])], inplace=True)
    month_sum.dropna(axis=1, inplace=True)

    

    # PUT IT ALL TOGETHER
    # append data only if not in Nov 2017 or Dec 2017 (since those two months are corrupted)
    if "November 2017" not in filename and "December 2017" not in filename:
        # append data
        months.append(month)
        month_sums.append(month_sum)

# glue data together
df = pd.concat(months, axis=0, ignore_index=True) #df = daily frame
mf = pd.concat(month_sums, axis=0, ignore_index=False) #mf = monthly frame

# [2] REMOVE EXTRANEOUS COLUMNS IN DF
# extraneous columns occur when a column is mistitled in a specific week.
# thus, we need to merge these extraneous columns with the columns where that data was *supposed* to go

# define a function which merges two columns
def merge_cols(d: pd.DataFrame, main_col: str, corrupted_col: str):

    # move any non-null values in the corrupted column to the main column
    d[main_col] = np.where(pd.isnull(df[corrupted_col]), df[main_col], df[corrupted_col])
    
    # remove the now-redundant corrupted column
    d = d.drop(columns=[corrupted_col], inplace=False)
    
    return d

# now, merge the columns
df = merge_cols(df, "Other/AMW", "Other")
df = merge_cols(df, "Day", "lth ")
df = merge_cols(df, "Automated Matches Total", 3)
df = merge_cols(df, "Automated Matches Total", 29)



# [3] EXPLICITY MARK HOLIDAYS AS HOLIDAYS IN DF
# the data that we are given includes the messages in the "Automated Matches Total" col. Why? no idea :/

# any values in the "Automated Matches Total" column with that is a string is a holiday
holiday_inds = df[df['Automated Matches Total'].apply(lambda x: isinstance(x, str))].index

for i in holiday_inds:
    # move holiday msg its own holiday column
    df.at[df.index[i], 'Holiday'] = df.at[df.index[i], 'Automated Matches Total']

    # clear the data in 'automated matches total'
    df.at[df.index[i], 'Automated Matches Total'] = np.nan



# [4] ORGANIZE DATA BY DATE

# sort data by date
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by=['Date'], inplace=True)

# convert index to date
df.set_index(['Date'], inplace=True)

# remove all data after 2019-07-12; the police stopped recording stats after this point
df = df.loc[:'2019-07-12']



# [5] CHANGE THE NAMES OF THE COLUMNS TO MAKE EM LOOK NICER <3

df.rename(inplace=True, columns={
    'Day': 'day', 
    'Automated Matches Total': 'automated_matches_total', 
    '1:R': '1:R', 
    'Multiples': 'multiples', 
    'Data Errors': 'data_errs',
    'Twins': 'twins',
    'Modified Criminal Cases': 'modified_crim_cases',
    'New Criminal Cases': 'new_crim_cases',
    'Photo Arrays': 'photo_arrs',
    'FR Requests': 'fr_reqs',
    'FR Matches': 'fr_matches',
    'Local': 'local',
    'State': 'state',
    'Federal': 'federal',
    'Other/AMW': 'other',
    'Root File': 'root file',
    'Holiday': 'holiday'
})


# [6] MAKE SURE STATE COLUMN IS A FLOAT CUZ FOR SOME REASON ITS NOT

def floatify(d): # converts a df cell value from string to float
    d = str(d).replace(' ', '')
    if d == '':
        return float('nan')
    else:
        return float(d)


df['state'] = df['state'].map(np.vectorize(floatify))
df['state'] = df['state'].astype(float)



# [7] EXPORT :D

# convert to files
df.to_csv('data/source_extract/daily_stats.csv', index=True)
mf.to_csv('data/source_extract/monthly_stats.csv', index=True) 
