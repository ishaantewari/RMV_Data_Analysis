import json
import datetime
import re
import datetime

# load files
def load_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()    
    return data



def write_file(object, file):
   # serialize
   json_object = json.dumps(object, indent=4)
   
   # write
   with open(file, "w") as outfile:
      outfile.write(json_object)

def is_empty(content):
    if content == None:
        return True
    condensed_string = content.replace(" ", "").replace("\n", "")
    if condensed_string == " " or condensed_string == "":
        return True
    else:
        return False

# find date slightly more easily

def find_date(year, month, day):

    months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    m = ""

    if type(month) is str:
        m = months[month]
    elif type(month) is int:
        m = month
    
    d = datetime.date(int(year), int(m), int(day))
    return d

# search for a regular expression in a given block of text
def search_for(regexs, text):
    for regex in regexs:
        match = re.search(regex, text)
        if match:
           return True
    
    return False


def binary_search(arr, low, high, x, name):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
        item = arr[mid]
        print(item["lastName"])
        print(item["lastName"] == name)
        # If element is present at the middle itself
        if item["finalDate"] == x and item["lastName"] == name:
            print("HERE")
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif item["finalDate"] > x:
            print("up")
            print(mid-1)
            return binary_search(arr, low, mid - 1, x, name)
 
        # Else the element can only be present in right subarray
        else:
            print("down")
            print(mid+1)
            return binary_search(arr, mid + 1, high, x, name)
 
    else:
        # Element is not present in the array
        return -1
    

 
 

def standardize_date(string):
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

    if string != "" and string != " ":
        raw_slashed_date = re.search("([0-3]?\d{1})\/((0|1|2)?\d{1})\/((19|20)\d{2})", string)
        if raw_slashed_date:
            date_props = raw_slashed_date.group().split("/")
            date = datetime.date(int(date_props[2]), int(date_props[0]), int(date_props[1]))
        else:
            # search for year, which is a four digit number that is BEFORE timezone
            year = re.search("\d\d\d\d", string)
            if year:
              year = year.group()
            else:
              year = 1
              #year = 1 is a placeholder
            # search for month, which contains letters; only include first 3 letters
            # e.g. jan, feb, mar
            words = re.findall("[a-zA-Z]\s*[a-zA-Z]\s*[a-zA-Z]", string)
            month = 13
            for word in words:
                trimmed_word = word.replace(" ", "")
                if trimmed_word in months.keys():
                  month = months[trimmed_word]
            if month != 13:
                
                # create dictionary for first three month letters -> month
                # minimum of three letters to define month to avoid repeats
                # search for date, which should be one-two digit 
                day = re.search("\D\d+", string).group()
                day = day[1:]
                #day = day[:-1]
                date = datetime.date(int(year), int(month), int(day))
            else:
                date = datetime.date(1, 1, 1)               
    else:
        date = datetime.date(1, 1, 1)
    return date

