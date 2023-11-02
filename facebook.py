from helpers import *
from fuzzywuzzy import fuzz

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
count = 0


array_logs = load_file('./source_extract/allLogs.json')
mails = load_file('./results.json')

temp_mails = []
bodies = []

removed_mails = 0
for email in mails:
    if email["body"] != None:
      match = search_for(["[fF]ace[bB]ook"], email['body'])
      if match and not(email["body"] in bodies):
        check = True
        for body in bodies:
            ratio = fuzz.ratio(email["body"], body)
            if ratio>90:
                check = False
        if check == True:
            temp_mails.append(email)
            bodies.append(email["body"])

print(len(temp_mails))
for t in temp_mails:
   print(t['body'] + '\n\n')
