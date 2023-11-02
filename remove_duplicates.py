from helpers import *
from fuzzywuzzy import fuzz
import re
import numpy as np

print("-> FIXING THE ISSUE THAT IS DUPLICATES WOO")

# load data
mails = load_file('cleaning_data/cleaned_mails.json')



# Add simplifiedBody to each mail to remove extraneous data when filtering out duplicates.
print("\n-> SIMPLIFYING MAIL BODIES AND SUBJECTS\n")

pct = 0
for i, mail in enumerate(mails):

    # calculate pct done with loop (for convenience in terminal)
    new_pct = int(i * 10 / len(mails)) * 10
    if new_pct != pct: 
        pct = new_pct
        print(f'{new_pct}%')


    # simplify mail body
    if not is_empty(mail['body']):
        # remove special chars
        sb = mail['body'].encode('ascii', 'ignore').decode('utf-8')
        
        # convert to lowercase
        sb = sb.lower()

        # remove emails separated by whitespace
        sb = re.sub(r'\s.*@.*(\.us|\.gov|gmail\.com|hotmail\.com)\s', '', sb)

        # remove spaces
        sb = sb.replace(' ', '')

        # paterns to remove
        rmv_ptrns = [
            # remove the signature, if it exists, and everything after
            r'(thanks|best|thankyou|respectfully|sincerely|thanksinadvance)(,).*', 

            # remove the confidentiality notice, if it exists, and everything after
            r'(confidential).*',

            # remove the header, if it exists, and everything before
            r'.*\(pol\)',
            r'.*(wrote:)',

            # remove emails bounded by <>
            r'<(\w|\.)+@(\w|\.)+>(;?)',

            # remove phone numbers
            r'(\+?)(1?)(-?)(\(?)\d\d\d(\)?)(\-?)\d\d\d(\-)\d\d\d\d',
            r'(cell(:?))|(desk(:?))|(fax(:?))|(office(:?))',

            # remove addresses (this takes too long lol)
            r'\d+\w+\w+\W+(al|ak|az|ca|co|ct|dc|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo|mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy|alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware|florida|georgia|hawaii|idaho|illinois|indiana|iowa|kansas|kentucky|louisiana|maine|maryland|massachusetts|michigan|minnesota|mississippi|missouri|montana|nebraska|nevada|newhampshire|newjersey|newmexico|newyork|northcarolina|northdakota|ohio|oklahoma|oregon|pennsylvania|rhode island|south carolina|south dakota|tennessee|texas|utah|vermont|virginia|washington|west virginia|wisconsin|wyoming)\d\d\d\d\d'
        ]


        # now, remove those patterns
        for rp in rmv_ptrns:
            re.sub(rp, '', sb)

        mail['simplifiedBody'] = sb
    else:
        mail['simplifiedBody'] = ""






# Identify which mail numbers are duplicates via a fuzzywuzzy similarity test between bodies
print("\n-> CHECKING DUPLICATES\n")

ratio_percentiles = np.zeros(11)
pct = 0
mails_to_rm = set()

for i, mail_1 in enumerate(mails):

    # calculate percentage done with loop (for convenience in terminal)
    new_pct = int(i * 10 / len(mails)) * 10
    if new_pct != pct: 
        pct = new_pct
        print(f'{new_pct}%')


    body_1 = mail_1['simplifiedBody']
    subj_1 = mail_1['simplifiedSubject']

    for mail_2 in filter(lambda x: x['year'] == mail_1['year'] and x['month'] == mail_1['month'] and x['day'] == mail_1['day'], mails):
        
        # first, mark which emails are duplicates according to their bodies
        # these emails will be removed later

        body_2 = mail_2['simplifiedBody']
        
        if body_1 != '' and body_2 != '':
            body_ratio = fuzz.ratio(body_1, body_2)
            ratio_percentiles[int(body_ratio / 10)] += 1

            # mark emails that have sufficiently high similarity score for removal
            if body_ratio > 90:
                mails_to_rm.add(mail_2['mailNo'])



# Now actually remove the duplicates, and get a list of duplicate-less mails!
print("\n-> REMOVING DUPLICATES\n")
new_mails = []

for mail in mails:
    # calculate percentage done with loop because it goes on forevah
    new_pct = int(i * 10 / len(mails)) * 10
    if new_pct != pct: 
        pct = new_pct
        print(f'{new_pct}%')


    if mail['mailNo'] not in mails_to_rm:
        new_mails.append(mail)


print(f'{len(mails_to_rm)} emails removed ({round(len(mails_to_rm) * 100 / (len(mails_to_rm) + len(mails)),2)}%). {len(mails)} mails left\n')
write_file(new_mails, 'mails_no_dups.json')



# get distribution of comparisons (to confirm that the regex expressions are actually narrowing down the search)
# when adding a new regex expresion to further simplify the mail/subject body, it is helpful to check this distribution before and after
# if the similarity scores move towards the externalities (0 and 100th percentile) after applying the regex exp, it was successful in improving the accuracy of fuzzywuzzy check!
print("~~~~~~~~~~~~~~~RATIO DISTRUBUTION~~~~~~~~~~~~~~~")
for i, rp in enumerate(ratio_percentiles):
    print(f'{i*10}: {round(rp * 100 / ratio_percentiles.sum(), 2)}%  |  {rp} comparisons')
