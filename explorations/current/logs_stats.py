from helpers import load_file
from helpers import write_file
from helpers import search_for
from helpers import findDate
import datetime 
from fuzzywuzzy import fuzz
from standarise_dates import standardize_date
months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

array_logs = load_file('./source_extract/allLogs.json')
dates = {}
logs = []

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

temp_logs = []
for log in logs:
        #adding lastName and date to logs
        name = log["officer"].split(" ")
        lastName = name[-1]
        log["lastName"] = lastName
        #find dates
        if log["day"].isnumeric() and log["year"].isnumeric() and log["month"].replace(" ", "") in months:
            day = findDate(log["year"], log["month"].replace(" ", ""), log["day"])
        else:
            day = findDate(1800, "January", 1)
        log["finalDate"] = day.year*10000+day.month*100+day.day

        temp_logs.append(log)
logs = temp_logs

for log in logs:
    date = log["finalDate"]
    date = int(date/100)
    dates[date] = 0


for log in logs:
    date = log["finalDate"]
    date = int(date/100)
    dates[date]+=1

print(dates)

#part two - stats recorded by rmv
dates_two = {}

import csv
with open('daily_stats.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        reqs = lines[10]
        if lines[0] != "Date":
            date = int(lines[0].replace("-", ""))
            date = int(date/100)
            dates_two[date]=0
    print("done")

with open('daily_stats.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        if lines[10] != "fr_reqs" and lines[10] != "" and lines[10] != " ":
            reqs = int(lines[10].split(".")[0])
        if lines[0] != "Date":
            date = int(lines[0].replace("-", ""))
            date = int(date/100)
            dates_two[date]+=reqs

print(dates_two)

# results
# from logs: {201601: 19, 201602: 14, 180001: 6, 201604: 10, 201605: 12, 201606: 17, 201607: 10, 201608: 18, 201609: 19, 201610: 22, 201611: 22,
# 201701: 32, 201702: 15, 201703: 31, 201704: 14, 201705: 20, 201706: 18, 201707: 19, 201708: 16, 201709: 14, 201710: 13, 201711: 6, 201712: 13, 201801: 18, 201802: 15, 201803: 17, 201804: 14, 201805: 12, 201806: 19, 201807: 8, 201808: 15, 201809: 12, 201810: 17, 201811: 22, 201812: 13, 201901: 12, 201902: 10, 201903: 9, 201904: 4, 201905: 11, 201908: 4}
# from stats: {201609: 29, 201610: 41, 201611: 47, 201612: 44, 201701: 56, 201702: 31, 201703: 45, 201704: 24, 201705: 42, 201706: 36, 201707: 30, 201708: 17, 201709: 18, 201710: 15, 201801: 32, 201802: 15, 201803: 29, 201804: 25, 201805: 21, 201806: 33, 201807: 15, 201808: 29, 201810: 20, 201811: 16, 201812: 25, 201901: 26, 201902: 26, 201903: 22, 201904: 15, 201905: 12, 201906: 0, 201907: 0}
# missing 201612 in logs
# consistently fewer recs logged than requested