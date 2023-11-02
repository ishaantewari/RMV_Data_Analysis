from helpers import *
from fuzzywuzzy import fuzz


logs = load_file('cleaning_data/cleaned_logs.json')
mails = load_file('cleaning_data/cleaned_mails.json')


# clean names
for log in logs:

    cleaned_full_name = log['officer'].strip().lower()
    names = cleaned_full_name.split(' ')


    temp_names = []
    for name in names:
        
        # remove empty names
        if not is_empty(name):
        
            # strip whitespace from names
            name = name.strip()

            # remove known titles
            titles = ['ice', 'patrolman', 'officer', 'patrolman', 'detective', 'special', 'ada', 'commander', 'sa', 'ago', 'inspector', 'deportation', 'office', 'p.o', 'agent', 'tfo', 'deporation office', 'tpr', 'cpt', 'msp', 'lt', 'lt.', 'jr.', 'usm']
            if name not in titles:
                temp_names.append(name)

    names = temp_names
    
    # remove periods: a period in the first element is a title (e.g. tpr., sgt.)
    # a period in the second to last element is a middle initial
    if names[0][-1] == '.':
        del names[0]

    if len(names) > 1 and names[-2][-1] == '.':
        del names[-2]


    # join the names back together, and put the cleaned info back into the log
    log['officer'] = ' '.join(names)
    
    # remove extraneous characters and phrases
    extraneous_ptrn = ['\"', '.', '\u2026', 'per johnson', 'n/a']
    for ptrn in extraneous_ptrn:
        log['officer'] = log['officer'].replace(ptrn, '')

    # fix this one name that doesnt go thru fuzz properly
    log['officer'] = log['officer'].replace('dawaatkinson', 'dana atkinson')



# remove logs with empty last names
temp_logs = []
for log in logs:
    if not is_empty(log['officer']):
        temp_logs.append(log)
logs = temp_logs
    

# do the fuzzy wuzzy similarity comparison; group the names together if they represent the same person
all_officer_names = []
for i1, log_1 in enumerate(logs):

    n1 = log_1['officer'].split(' ')
    l1 = n1[-1] # last name #1
    
    possible_names = [n1]

    for i2, log_2 in enumerate(logs):
        n2 = log_2['officer'].split(' ')
        l2 = n2[-1] # last name #2

        lr = fuzz.ratio(l1, l2) # ratio between last names
        
        # if the last names are similar...
        if lr > 90: # <- <- <- THE LAST NAME THRESHOLD IS SET HERE
            
            # if both names have a first name, compare those as well
            if len(n1) > 1 and len(n2) > 1:
                f1 = n1[-2] # first name #1
                f2 = n2[-2] # first name #2
             
                fr = fuzz.ratio(f1, f2) # ratio between first names

                if fr > 50: # <- <- <- THE FIRST NAME THRESHOLD IS SET HERE
                    if fr < 100 or lr < 100:
                        possible_names.append(n2)
                    logs.pop(i2)
                    

            # if one of the names doesn't have a first, then only compare the last names
            else:
                if lr > 98:
                    if fr < 100 or lr < 100:
                        possible_names.append([n2])
                    logs.pop(i2)

    # remove other middle names/initials
    for pn in possible_names:
        if len(pn) > 2:
            pn = [pn[0], pn[-1]]

    all_officer_names.append(possible_names)

write_file(all_officer_names, 'all_officer_names.json')
