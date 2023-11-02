from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
import datetime 
from standarise_dates import standardize_date

months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
count = 0


# format is from _ import _

count = 0
logs = [] #will be the list of logs w/o fax, walk-in etc

array_logs = load_file('./source_extract/allLogs.json')
mails = load_file('./source_extract/allMails.json')


# [2] CLEAN UP LOGS 

# (a) dictionaries!
for array_log in array_logs[1:]:
    logs.append({
        "number": array_log[0],
        "year": array_log[1],
        "month": array_log[2],
        "day": array_log[3],
        "officer": array_log[4],
        "agency": array_log[5],
        "office": array_log[6],
        "location": array_log[7],
        "reqMethod": array_log[8],
        "reqNum": array_log[9],
        "reqMatch": array_log[10],
        "photoAry": array_log[11],
        "other": array_log[12],
        "notes": array_log[13]
    })




# (b) get rid of non-email logs and add date and lastName
temp_logs = []
removed_logs = 0
for log in logs:
    if search_for(["(?i)fax", "(?i)walk-?\s?in", "(?i)phone"], log["reqMethod"]):
        removed_logs += 1
        #print(log)
    elif log["reqMethod"] == " " or log["reqMethod"] == "":
        removed_logs += 1
    else:
        #adding lastName and date to logs
        name = log["officer"].split(" ")
        lastName = name[-1]
        log["lastName"] = lastName
        #find dates
        if log["day"].isnumeric() and log["year"].isnumeric() and log["month"].replace(" ", "") in months:
            day = findDate(log["year"], log["month"].replace(" ", ""), log["day"])
        else:
            day = 0
        log["finalDate"] = day

        temp_logs.append(log)
logs = temp_logs

print(str(removed_logs) + " logs removed. Reason: in-person. " + str(len(logs)) + " logs left.")

# [4] REMOVE ALL INSTANCES OF "LICENSE REVOKED" FROM REMAINING DATA; THESE EMAILS ARE NOT SUSPICIOUS
temp_mails = []
removed_mails = 0
for email in mails:
    if email["body"] != None:
      match = search_for(["(?i)li\wen\we\s?revoc?ked"], email['body'])
      if match:
          removed_mails+=1
          #print(email)
      else:
        temp_mails.append(email)
    else:
       temp_mails.append(email)

mails = temp_mails
temp_mails = []
removed_mails = []

# [5] MATCH EMAILS TO LOGS
# (a) adding a lastName and finalDate property to mails and remove special characters
for mail in mails:
  #find last name
        # add a lastName property to each mail in mails
    name = mail['from'].strip().lower()

    possible_names = []

    if not (name == "" or name == None or name == " " or int(mail['mailNo']) in [3787, 5832]):
        if "," in name:
            possible_names.append(name.split(",")[0])
        elif "commonweal" in name or "fusion center" in name:
            possible_names.append("Commonwealth Fusion Center")
        elif "Massachusetts State Police Records Management System" in name:
            possible_names.append(
                "Massachusetts State Police Records Management System")
        elif "ACISS (Massachusetts State Police)" in name:
            possible_names.append("ACISS (Massachusetts State Police)")
        else:
            name = name.split(' ')
            if len(name) == 1:
                possible_names.append(name[0].split('@')[0])
            else:
                blacklisted_parts = ['<', "(pol", "(dot", "(bri", "(dod", "@"]
                temp = []
                for part in name:
                    check = True
                    for blacklisted in blacklisted_parts:
                        if blacklisted in part:
                            check = False

                    if check == True:
                        temp.append(part)

                possible_names = (temp)

    if len(possible_names) > 0:
        mail["lastName"] = possible_names
    else:
        mail["lastName"] = ["none"]


  #find dates
    tempdate = mail["date"]
    if tempdate != None and mail["body"] != None:
        date = standardize_date(tempdate)
        mail["finalDate"] = date.year*10000+date.month*100+date.day
        #mail["body"] = (mail["body"].encode('ascii', 'ignore')).decode("utf-8")    #FOR SPECIAL CHARS

        temp_mails.append(mail)
    else:
        removed_mails.append(mail)

removed=0
mails = temp_mails
# (b) sorting the list of emails by date - might make the matching a little faster
mails = sorted(mails, key=lambda x: x['finalDate'])


      


# (c) check against the emails

count = 0
for log in logs:
  date = log["finalDate"]
  name = log["lastName"]
  for mail in mails:
    if name in mail["lastName"] and mail["finalDate"] == date:
        log["email"] = mail["mailNo"]
        break
    elif mail["mailNo"] == 6661:
       log["email"] = -1
       count+=1

true = 0
false = 0


# [6] write to results file

write_file(mails, "results.json")

f.close()
