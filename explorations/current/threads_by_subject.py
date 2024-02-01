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

mails = load_file('./results.json')

subjects_to_mails = {} #will be in format {subject(s): [all associated mail nos]}
subjects = [] #list of all subjects used so far
for mail in mails:
    if mail["subject"] != None and mail["subject"] != "":
        subject = mail["subject"]
        subject = ''.join(ch for ch in subject if ch.isalnum())
        subject = subject.lower().replace(" ", "").replace("re:", "").replace("fw:", "").replace("re", "").replace("fw", "")
        mailNo = mail["mailNo"]
        check = False
        if subject in subjects:
                subjects_to_mails[subject].append(mailNo)
                check = True
        if check == False:
            subjects_to_mails[subject] = [mailNo]
            subjects.append(subject)


print(subjects_to_mails.keys())

print(subjects_to_mails)
print(len(subjects_to_mails))

