import numpy as np
from nameparser import HumanName
from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
import datetime 
from standarise_dates import standardize_date

logs = load_file('./final_logs.json')
mails = load_file('./results.json')

toremove = [] # list of mailNos of duplicates
count = 0


for mail in mails:
    name = HumanName(mail["from"])
    print(name.last)