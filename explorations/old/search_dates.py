from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
import datetime 
from fuzzywuzzy import fuzz
from standarise_dates import standardize_date

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
count = 0


# format is from _ import _

count = 0
logs = [] #will be the list of logs w/o fax, walk-in etc

array_logs = load_file('./source_extract/allLogs.json')
mails = load_file('./subject_mails.json')

toremove = [] # list of mailNos of duplicates
count = 0

subject = ""
request_mails = []
bodies = []
subjects = []
count = 0

for mail in mails:
    date = int(mail["finalDate"])
    if date >= 20161200 and date <= 20170100: #and mail["subject"] not in subjects:
        count+=1
        print(mail["mailNo"])
        print(mail["body"])
        print(mail["from"])
        print(mail["finalDate"])
        subjects.append(mail["subject"])
        print(" ")

print(len(mails))
print(count)



# emails within period: 4633, 5466, 3406, 5998, 3378