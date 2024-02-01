"""
PERFORMS A ROUGH CLEAN ON ALL THE DATA FROM SOURCE_EXTRACTS
- all data is sent to cleaning_data; the data is separated into 'cleaned' and 'uncleaned' depending on if this file was able to clean it
- uncleaned files are handled in handle_uncleaned_data.py manually (which doesnt exist yet :P)
"""

#TODO: REMOVE COPY BODY EMAILS--should also check that the logs are good
#TODO: figure out what photo array is
#TODO: do we want to include email and phone req methods? because rn they arent being included

import sys
sys.path.append('../NewtonHS_RMV_emails')


from helpers import *


print("\n-> CLEANING DATA\n")

# [1] IMPORT LOGS INTO PYTHON

logs = []

array_logs = load_file('data/source_extract/allLogs.json')
mails = load_file('data/source_extract/allMails.json')


# convert logs to dictionaries, and add a 'toBeRemoved' property to each mail
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
        "notes": array_log[13],
        "toBeRemoved": False,
    })

for mail in mails:
    mail['toBeRemoved'] = False




temp_logs = []

removed_logs = []
uncleaned_logs = []
uncleaned_mails = []

# [2] Define helper functions

# first, define a function that adds a log/mail to the uncleaned_logs/uncleaned_mails array and flags it for removal
def mark_as_uncleaned(data, reason_why_uncleaned):
    data['toBeRemoved'] = True

    # if the data is already in uncleaned_logs/uncleaned_mails, no need to append it; just add the error statement onto the reasonWhyUncleaned property
    if 'reasonWhyUncleaned' in data:
        
        if "reqMethod" in data:
            # find the uncleaned_log with matching # as data
            did_find_log = False
            for uncleaned_log in uncleaned_logs:
                if uncleaned_log['number'] == data['number'] and uncleaned_log['year'] == data['year']:
                    # add reason_why_uncleaned to that log
                    uncleaned_log['reasonWhyUncleaned'] += ", " + reason_why_uncleaned
                    did_find_log = True
                    break
            
            if not did_find_log:
                print(f"ERROR: COULD NOT FIND LOG NUMBER {data['number']} IN UNCLEANED DATA. \n DATA: {data}")

        elif "mailId" in data:

            did_find_mail = False
            for uncleaned_mail in uncleaned_mails:
                if uncleaned_mail['mailNo'] == data['mailNo']:
                    # add reason_why_uncleaned to that log
                    uncleaned_mail['reasonWhyUncleaned'] += ", " + reason_why_uncleaned
                    did_find_mail = True
                    break
            
            if not did_find_mail:
                print(f"ERROR: COULD NOT FIND MAIL NUMBER {data['number']} IN UNCLEANED DATA. \n DATA: {data}")
        
        else:
            print("ERROR: DATA COULD NOT BE MARKED AS UNCLEANED; COULD NOT IDENTIFY IF LOG OR EMAIL")

        
    else:
        data['reasonWhyUncleaned'] = reason_why_uncleaned

        if "reqMethod" in data:
            uncleaned_logs.append(data)
        elif "mailId" in data:
            uncleaned_mails.append(data)
        else:
            print("ERROR: DATA COULD NOT BE MARKED AS UNCLEANED; COULD NOT IDENTIFY IF LOG OR EMAIL")


# also, define a function to clean flagged data before removal
def clean_flagged_data(flagged_data, uncleaned_data):
    cleaned_data = flagged_data[:]
    cleaned_data = list(filter(lambda d: (d['toBeRemoved'] == False), cleaned_data))

    # if data is mail, sort it j to make life a bit easier
    if 'mailId' in cleaned_data[0]:
        cleaned_data = sorted(cleaned_data, key=lambda x: (x['year'], x['month'], x['day']))

    for c in cleaned_data:
        c.pop('finalDate', None)
        c.pop('toBeRemoved', None)
    
    for u in uncleaned_data:
        u.pop('finalDate', None)
        u.pop('toBeRemoved', None)

    return [cleaned_data, uncleaned_data]


# [3] Get rid of non-email logs
for log in logs:
    if not search_for(["(?i)e-?\s?mail"], log["reqMethod"]):
        removed_logs.append(log)
        log['toBeRemoved'] = True
    # if False:
    #     continue
   

# [4] clean properties, including the addition of lastName and finalDate, to logs ; if cannot obtain these properties, mark as uncleaned

    else:
        # clean lastName property
        names = log["officer"].strip().split(" ")
        names = [n.strip() for n in names]
        last_name = names[-1].lower()
        
        if not is_empty(last_name):
            log["lastName"] = last_name
        else:
           mark_as_uncleaned(log, "empty last name")

        # clean finalDate property
        months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

        if log["day"].isnumeric() and log["year"].isnumeric() and log["month"].replace(" ", "") in months:
            log['year'] = int(log['year'])
            log['month'] = months[log['month'].replace(" ", "")]
            log['day'] = int(log['day'])

        else:
            mark_as_uncleaned(log, "date error")

        # clean the rest of the properties lol
        # NOTE: if reqNum or reqMatch are not provided, we are setting them to zero now

        if log['number'].isnumeric() and int(log['number']) >= 1:
            log['number'] = int(log['number'])
        else:
            mark_as_uncleaned(log, "log number err")

        if log['reqNum'].isnumeric():
            log['reqNum'] = int(log['reqNum'])
        elif is_empty(log['reqNum']):
            log['reqNum'] == 0
        else:
            mark_as_uncleaned(log, "reqNum err")  

        if log['reqMatch'].isnumeric():
            log['reqMatch'] = int(log['reqMatch'])
        elif is_empty(log['reqMatch']):
            log['reqMatch'] == 0
        else:
            mark_as_uncleaned(log, "reqMatch err")        


# [5] send the cleaned logs to cleaned_logs.json, send the uncleaned logs to uncleaned_logs.json

cleaned_logs, uncleaned_logs = clean_flagged_data(logs, uncleaned_logs)


# [6] clean mail properties, inclduing adding lastName and finalDate properties; if cannot calculate these properties, send the mails to uncleaned_mails.json

# (a) adding a lastName and finalDate property to mails
dates = []
for mail in mails:
  
  # add a lastName property to each mail in mails
    name = mail['from'].strip().lower()
    
    possible_names = []
    
    if is_empty(name):
        mark_as_uncleaned(mail, 'empty name')
    
    elif int(mail['mailNo']) in [3787, 5832]:
        mark_as_uncleaned(mail, "custom name error- requires manual editing")
    
    
    elif "," in name:
        possible_names.append(name.split(",")[0])
    elif "commonweal" in name:
        possible_names.append("Commonwealth Fusion Center")
    elif "fusion" in name:
        possible_names.append("Fusion")
    elif "Massachusetts State Police Records Management System" in name:
        possible_names.append("Massachusetts State Police Records Management System")
    elif "ACISS (Massachusetts State Police)" in name:
        possible_names.append("ACISS (Massachusetts State Police)")
    else:
        name = name.split(' ')
        if len(name) == 1:
            possible_names.append(name[0].split('@')[0])
            print(name[0].split('@')[0])
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
            # print(name, possible_names, sep='\n')
            # print('\n')



    if len(possible_names) > 0:
        mail["possibleNames"] = possible_names
    else:
        mark_as_uncleaned(mail, "empty last name")


  # add a finalDate property to each mail in mails
    tempdate = mail["date"]
    if not is_empty(tempdate):
        date = standardize_date(tempdate)
        if date.year != 1:
            mail['year'] = date.year
            mail['month'] = date.month
            mail['day'] = date.day
        else:
            mark_as_uncleaned(mail, "invald date")
    else:
        mark_as_uncleaned(mail, "empty date")


cleaned_mails, uncleaned_mails = clean_flagged_data(mails, uncleaned_mails)



# [7] PRINT ALL THE INFO; WRITE TO FILES

print("~~~~~~~~~~~~~~~DATA CLEANED~~~~~~~~~~~~~~~\n")

print(str(round(len(cleaned_logs) * 100 / (len(cleaned_logs) + len(uncleaned_logs)),2)) + "% LOGS CLEANED")
print(len(cleaned_logs),  "logs cleaned.", len(uncleaned_logs) , "logs uncleaned.", len(removed_logs),  "logs removed for being in-person")
print("\n")

print(str(round(len(cleaned_mails) * 100 / (len(cleaned_mails) + len(uncleaned_mails)),2)) + "% MAILS CLEANED")
print(len(cleaned_mails), "emails cleaned.", len(uncleaned_mails), "emails uncleaned.") 
print('\n\n')


# write_file(cleaned_logs, 'cleaning_data/cleaned_logs.json')
# write_file(uncleaned_logs, 'cleaning_data/uncleaned_logs.json')
# write_file(cleaned_mails, 'cleaning_data/cleaned_mails.json')
# write_file(uncleaned_mails, 'cleaning_data/uncleaned_mails.json')
# write_file(cleaned_logs, 'data/other_data/cleaned_logs_with_non_emails.json')
