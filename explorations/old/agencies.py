#to find agencies 

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
agencies = {}
ag_list = []

for log in logs:
    agency = log["agency"]
    print(agency)
    if agency in ag_list:
        agencies[agency] = agencies[agency]+1
    else:
        agencies[agency] = 1
        ag_list.append(agency)

print(agencies)