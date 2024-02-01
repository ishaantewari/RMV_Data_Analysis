import re
from helpers import search_for
import datetime


months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}



def standardize_date(string):
    if string != "" and string != " ":
        raw_slashed_date = re.search("([0-3]?\d{1})\/((0|1|2)?\d{1})\/((19|20)\d{2})", string)
        if raw_slashed_date:
            date_props = raw_slashed_date.group().split("/")
            date = datetime.date(int(date_props[2]), int(date_props[0]), int(date_props[1]))
        else:
            # search for year, which is a four digit number that is BEFORE timezone
            year = re.search("\d\d\d\d", string)
            if year:
              year = year.group()
            else:
              year = 1
              #year = 1 is a placeholder
            # search for month, which contains letters; only include first 3 letters
            # e.g. jan, feb, mar
            words = re.findall("[a-zA-Z]\s*[a-zA-Z]\s*[a-zA-Z]", string)
            month = 13
            for word in words:
                trimmed_word = word.replace(" ", "")
                if trimmed_word in months.keys():
                  month = months[trimmed_word]
            if month != 13:
                
                # create dictionary for first three month letters -> month
                # minimum of three letters to define month to avoid repeats
                # search for date, which should be one-two digit 
                day = re.search("\D\d+", string).group()
                day = day[1:]
                #day = day[:-1]
                date = datetime.date(int(year), int(month), int(day))
            else:
                date = datetime.date(1, 1, 1)               
    else:
        date = datetime.date(1, 1, 1)
    return date

