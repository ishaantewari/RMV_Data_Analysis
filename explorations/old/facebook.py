from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
from fuzzywuzzy import fuzz
import datetime 
from standarise_dates import standardize_date

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
count = 0


array_logs = load_file('./source_extract/allLogs.json')
mails = load_file('./results.json')


temp_mails = []
emails = []

for email in mails:
    if email["body"] != None:
      match = search_for(["[fF]ace[bB]ook"], email['body'])
      if match:
        check = True
        for mail2 in emails:
            ratio = fuzz.ratio(email["body"], mail2["body"])
            if ratio>80 and mail2["finalDate"] == email["finalDate"]:
                check = False
        if check == True:
            temp_mails.append(email)
            emails.append(email)
            print(email["body"])
            print(" ")

print(len(temp_mails))