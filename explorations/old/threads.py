from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
from fuzzywuzzy import fuzz

import datetime 
from standarise_dates import standardize_date

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
count = 0


# format is from _ import _

count = 0
logs = [] #will be the list of logs w/o fax, walk-in etc

array_logs = load_file('./source_extract/allLogs.json')
mails = load_file('./results.json')

#[7] THREADS
#(a) sort out by lastNames

names_to_mails = {} #will be in format {lastName(s): [all associated mail nos]}
names = [] #list of all last names used so far
for mail in mails:
    name = mail["lastName"]
    mailNo = mail["mailNo"]
    check = False
    for option in name:
        option = ''.join(e for e in option if e.isalnum())
        if option in names:
            names_to_mails[option].append(mailNo)
            check = True
    if check == False:
        name[0] = ''.join(e for e in name[0] if e.isalnum())
        if len(name[0]) > 11:
            name[0] = " "
        else:
            names_to_mails[name[0]] = [mailNo]
            names.append(name[0])


print(names_to_mails.keys())
print(len(names_to_mails))

