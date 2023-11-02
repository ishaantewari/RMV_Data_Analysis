from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
import datetime 
from fuzzywuzzy import fuzz
from standarise_dates import standardize_date

# format is from _ import _

logs = load_file('./final_logs.json')
mails = load_file('./subject_mails.json')
mails_to_logs = {}

for log in logs:
    date = log["finalDate"]
    sender = log["lastName"]
    check = False
    finalmail = ""
    samedate = 0
    for mail in mails:
        if int(mail["finalDate"]/100) == int(date/100):
            samedate+=1
            if sender in mail["from"]:
                finalmail = mail
                mails_to_logs[mail["mailNo"]] = log["number"]
                check = True
                break
    print(samedate)
    #if not check:
        #print("_________________")
        #print(sender)
        #print(finalmail["from"])


print(len(logs))
print(len(mails_to_logs))
