from helpers import *
from fuzzywuzzy import fuzz

logs = load_file('cleaning_data/cleaned_logs.json')
mails_no_dups = load_file('mails_no_dups.json')


# Part 1: remove any emails that contain 're:', 'fwd:', etc. in the subject line
head_mails = []
for mail in mails_no_dups:
    subj = mail['subject']
    if not is_empty(subj) and not search_for(['re:', 'fw:', 'fwd:'], subj.lower()):
        head_mails.append(mail)



# PART 2: REMOVE DUPLICATE SUBJECTS
# this cannot be done in remove_duplicates.py because two replies to the same thread will be a false positive match
# however, because we want to remove all replies/fwds to isolate the heads of emails, it is fine to do so in this file

# # first, simplify mail subjects
# for mail in head_mails:
    
#     if not is_empty(mail['subject']):
#         # remove special chars
#         sb = mail['subject'].encode('ascii', 'ignore').decode('utf-8')
            
#         # convert to lowercase
#         sb = sb.lower()

#         # remove emails separated by whitespace
#         sb = re.sub(r'\s.*@.*(\.us|\.gov|gmail\.com|hotmail\.com)\s', '', sb)

#         # remove spaces
#         sb = sb.replace(' ', '')

#         # remove emails bounded by <>
#         sb = re.sub(r'<(\w|\.)+@(\w|\.)+>(;?)', '', sb)

#         # remove 're:', 'fw:', etc.
#         sb = re.sub(r'(re:)|(fw:)|(fwd:)', '', sb)
        

#         mail['simplifiedSubject'] = sb
#     else:
#         mail['simplifiedSubject'] = ''

# # mark similar mails for removal
# mails_to_rm = set()

# for mail_1 in head_mails:
#     subj_1 = mail_1['simplifiedSubject']
#     for mail_2 in filter(lambda x: x['year'] == mail_1['year'] and x['month'] == mail_1['month'] and x['day'] == mail_1['day'], head_mails):
#         subj_2 = mail_2['simplifiedSubject']
        
#         if subj_1 != '' and subj_2 != '':
#             r = fuzz.ratio(subj_1, subj_2)
#             if r == 100:
#                     mails_to_rm.add(mail_2['mailNo'])
#                     print(mail_2['mailNo'], r, ':', subj_1, subj_2,)

# print(len(mails_to_rm), len(head_mails))

# # now actually remove duplicates for realises
# no_dups_head_mails = []
# for mail in head_mails:
#      if mail['mailNo'] not in mails_to_rm:
#         no_dups_head_mails.append(mail)
#         print(mail)
            


write_file(head_mails, 'test.json')
print(len(head_mails))

        

