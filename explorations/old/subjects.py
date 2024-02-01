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
mails = load_file('./results.json')

toremove = [] # list of mailNos of duplicates
count = 0

subject = ""
request_mails = []
bodies = []
subjects = []
duplicates = 0

for mail in mails:
    subject = mail["subject"]
    if subject != None:
        if "RE:" in subject or "re:" in subject or "Re:" in subject or "FW:" in subject or "fw:" in subject or "Fwd:" in subject or "Fw:" in subject:
            a=0
        else:
            body = mail["body"]
            check = True
            #if subject in subjects:
                #for body_two in bodies:
                    #ratio = fuzz.ratio(body, body_two)
                    #if ratio>70:
                        #check = False
            if check == True:
                print("_________________")
                print(subject)
                request_mails.append(mail)
                bodies.append(body)
                subjects.append(subject)
                print(mail["to"])
                print(mail["from"])

print("lengths:")
print(len(mails))
print(len(request_mails))
print("number of duplicates:")
print(duplicates)
write_file(request_mails, "subject_mails.json")
