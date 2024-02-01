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
            body = mail["body"]
            if "case" in body.lower() or "investigation" in body.lower():
                count = 1
            else:
                if mail["from"] != None and mail["to"] != None and mail["cc"] != None: 
                    if sender.lower() in mail["from"].lower() or sender.lower() in mail["cc"].lower() or sender.lower() in mail["to"].lower():
                        finalmail = mail
                        mails_to_logs[mail["mailNo"]] =  int(log["number"])+int(log["year"])*1000
                        check = True
                        break
                if mail["from"] != None and mail["to"] != None:
                    if sender.lower() in mail["from"].lower() or sender.lower() in mail["to"].lower():
                        finalmail = mail
                        mails_to_logs[mail["mailNo"]] = int(log["number"])+int(log["year"])*1000
                        check = True
                        break
    if not check:
        print("_________________")
        print(log)
        #print(finalmail["from"])

print(len(logs))
print(len(mails_to_logs))
print(mails_to_logs)