# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 19:31:34 2020

@author: Sanjana
"""

# https://pastebin.com/PNmkzNYk
"""
Challenges in the raw CDR data needed to handled or processed

1. No column name   
   ( header = None )
    column no -  actual name
    1            serviceProvider
    5            direction
    9            startTime
    13           EndTime
    120          userId 
    180          twoStageDialingDigits
    146          relatedCallId
    147          relatedCallIdReason
    267          vpDialingfacResult
    312          locationType
    345          userAgent


2 . Columns (6,8,20,29,69,71,73,75,77,99,119,126,133,134,148,152,
         174,179,181,194,195,196,200,274,304,307,313,
         319,346,409,412,434,442) have mixed types
    ( lowmemory = false )

3. Column 9 and 13 contains date and time information in regular pattern like- 
    "20190620032717.906". col 9 - start date and col 13 - end date
    First 8 characters represents Date
    Rest characters represents Time
    2019 year, 06 month, 20 day, 03 hours, 27 minutes, 17 sec
    ( function datetime_divider )
    
4. Column 5, 267, 312 contains a simple name for a Standard Terminologies

5. Column 312 conatins some unmwanted data other than the main data in it

6. Column 147 contains all the services/feature offered but some services are
    also distributed among column 267, 312 which are needed to be in col 147.
    
7. No information about the start and end of the call and total duration of the
    call

8. No hour wise distribution and week wise distribution of the calls 
    
"""


import pandas as pd
import numpy as np
import re
import datetime

#  Function to seperate the date and time from column 9
def datetime_divider(data):
    # data type of data is list
    # ["20190620032717.906"]
    for index in range(len(data)):    
        # find the digit if at begining only not others
        if re.match("^\d", str(data[index])): 
            regex = re.compile("\d{1,8}") 
            a = regex.findall(str(data[index]))
            data[index] = [a[0], a[1]]
        else:
            data[index] = [np.nan, np.nan]
        
    return data


fruits = ['lemon', 'pear', 'watermelon', 'tomato']
print(fruits[0],fruits[1], fruits[2], fruits[3])

# unpacking the data
print(*fruits)


# List of tuples
pairs =  [ (1,'a'), (2,'b'), (3,'c'), (4,'d') ]

print(pairs)

numbers, letters = zip(*pairs)

print(type(numbers))

print(numbers) # Tuple of integer

print(type(letters))

print(letters)  # tuple of strings



data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
print(re.match("^\d", str(data[0])))

data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
print(re.match("^\d", str(data[2])))


data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
regex = re.compile("\d{1,8}") 
a = regex.findall(str(data[0]))
print(a)
          

data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
regex = re.compile("\d{1,8}") 
a = regex.findall(str(data[2]))
print(a)
            

# List of String 
data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
print(datetime_divider (data) )
# List of List
# [['20190620', '032717'], ['20190620', '052652'], [nan, nan], ['20190620', '052735']]


data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
print(*datetime_divider (data) )
# ['20190620', '032717'] ['20190620', '052652']  [nan, nan], ['20190620', '052735'] 


data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
result = zip(*datetime_divider (data))
print(list(result))
# List of tuples
# [('20190620', '20190620', nan, '20190620'), ('032717', '052652', nan, '052735')]


data = ["20190620032717.906", "20190620052652.52",'' ,"20190620052735.207"]
date,time = zip(*datetime_divider (data))
# ('20190620', '20190620', nan, '20190620')
# ('032717', '052652', nan, '052735')
print(type(date))
print(date)
print(type(time))
print(time)






# Function to convert the data in desired date format
def date_modifier(data):
    # data type of data is list
    # 20190620 should be converted to 2019-06-20
    for index in range(len(data)):
        if re.match("^\d", str(data[index])):
            year = str(data[index][:4])
            month = str(data[index][4:6])
            day = str(data[index][6:])
            data[index] = "-".join([year, month, day])
        else:
            data[index] =  np.nan
    return data


data = ['20190620', '20190620', np.nan, '20190620']
# List of string with date
# Return of formatted date
result = date_modifier (data)
print(result)
# ['2019-06-20', '2019-06-20', nan, '2019-06-20']






# Function to convert the data in desired datetime format
def time_modifier(data):
    # Data type of data is list
    # 032717 should be converted into 03:27:17 AM
    for index in range(len(data)):
        data[index] = str(data[index])
        if re.match("^\d", data[index]):
            hours = int(data[index][:2])
            minutes = data[index][2:4]
            sec = data[index][4:]
            
            if hours >=12:
                if hours == 12:
                    hr = str(hours)
                else:
                    hr = str(hours-12)
                meridiem = "PM"
            else:
                if hours == 0:
                    hr = str(12)
                else:
                    hr = data[index][:2]
                meridiem = "AM"
            
            data[index] = ":".join([hr, minutes, sec]) + " " + meridiem
        else:
            data[index] = np.nan
    return data


# List of string with time
# Return of formatted time
data = [ '032717', '052652', np.nan, '052735']
result = time_modifier (data)
print(result)
#['03:27:17 AM', '05:26:52 AM', nan, '05:27:35 AM']




def replace_simple_with_Standard_terminology(dataset):
    # This part replace the data with standard terminologies in col 5, 267, 312
    # Replacing String in the columns with standard Terminology
    dataset[5] = dataset[5].replace("Originating", "Outgoing")
    dataset[5] = dataset[5].replace("Terminating", "Incoming")
    
    dataset[267] = dataset[267].replace("Success", "Voice Portal")

    dataset[312] = dataset[312].replace("Shared Call Appearance", "Secondary Device")
    
    return dataset
    


def remove_Unwanted_data(dataframe):
    # data type of data is list
    for index in range(len(dataframe)):
        if dataframe[index] == "Secondary Device" or dataframe[index] =="Primary Device":
            continue
        else:
            dataframe[index] = np.nan 
    return dataframe




# This part sets all the services in one column 147
def combine_All_Services(data1, data2, data3):

    for index in range(len(data1)):
        if data1[index] is np.nan:
            
            if data2[index] is not np.nan and data3[index] is not np.nan:
                data1[index] = str(data2[index])+ "," + str(data3[index])
            
            elif data2[index] is not np.nan:
                data1[index] = data2[index]
            
            else:
                data1[index] = data3[index]
            
        else:
            continue
    return data1
    

data1 = ['Primary Device','Simultaneous Ring Personal', 'Secondary Device','Remote Office', 'Simultaneous Ring Personal']
data2 = ['Primary Device', 'Secondary Device','Primary Device', 'Secondary Device', 'Primary Device']    
data3 = ['Voice Portal']
result = combine_All_Services(data1,data2,data3)
print(result)



# Convert data into a specific format
def call_time_fetcher(data):

    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!="nan":
            year = data[index][:4]
            month = data[index][4:6]
            day = data[index][6:8]
            hours = data[index][8:10]
            minutes = data[index][10:12]
            seconds = str(round(float(data[index][12:])))
            if int(seconds) >= 60:
                seconds = int(seconds) -60
                minutes = int(minutes)+1 
            if int(minutes) >=60:
                hours = int(hours)+1
                minutes  = int(minutes) - 60 
            data[index] = f"{year}-{month}-{day} {hours}:{minutes}:{seconds}"
        else:
            data[index] = np.nan
    return data


data = ["20190620032717.906", "20190620052652.52",'nan' ,"20190620052735.207"]
result = call_time_fetcher (data)
print(result)


def hourly_range(data):
    # Time column data is passed as a list
    # 03:27:17 AM'
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!="nan":
            if re.search("PM", data[index]):
                time_data =  re.findall("\d+", data[index])
                if time_data[0] != "12":
                    time_data = int(time_data[0]) + 12
                else:
                    time_data = time_data[0]
                
            else:
                time_data =  re.findall("\d+", data[index])
                if int(time_data[0]) == 12:
                    time_data = f"0{int(time_data[0]) - 12}"
                else:
                    time_data = time_data[0]
                
                
            data[index] = f"{time_data}:00 - {time_data}:59"
        else:
            data[index] = np.nan
    return data

data = ['03:27:17 AM', '05:26:52 AM', 'nan', '05:27:35 AM']
result = hourly_range(data)
print(result)


def weekly_range(data):
    # Date column data is passed as a list
    # '2019-06-20' 
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index] != "nan":
            year, month, day = [int(x) for x in data[index].split("-")]
            result = datetime.date(year, month, day)
            data[index] = result.strftime("%A")
        else:
            data[index] = np.nan
    return data

data = ['2019-06-20', '2019-06-20', 'nan', '2019-06-20']
result = weekly_range(data)
print(result)


'''
    
1. No column name   
   ( header = None )
    column no -  actual name
    1            serviceProvider
    5            direction
    9            startTime
    13           EndTime
    120          userId
    180          twoStageDialingDigits
    146          relatedCallId
    147          relatedCallIdReason
    267          vpDialingfacResult
    312          locationType
    345          userAgent
'''


dataset_name = "raw_cdr_data.csv"                
raw_cdr_data  = pd.read_csv(dataset_name,header= None, low_memory= False)
    


'''
    Column 9 and 13 contains date and time information in regular pattern like- 
    "20190620032717.906". col 9 - start date and col 13 - end date
    First 8 characters represents Date
    Rest characters represents Time
    2019 year, 06 month, 20 day, 03 hours, 27 minutes, 17 sec
    
    function datetime_divider will break into 2 parts
    20190620
    032717
'''    
    
    
print(raw_cdr_data[9].tolist()[3])


# Creates 2 columns to store date and time
raw_cdr_data["date"], raw_cdr_data["time"] = zip(*datetime_divider(raw_cdr_data[9].tolist()))
       

print(raw_cdr_data["date"].tolist()[0])
print(raw_cdr_data["time"].tolist()[0])

raw_cdr_data['date'] = date_modifier(raw_cdr_data["date"].tolist())
raw_cdr_data["time"] = time_modifier(raw_cdr_data["time"].tolist())
    
print(raw_cdr_data["date"].tolist()[0])
print(raw_cdr_data["time"].tolist()[0])
    
 
    
    
'''
This part replace the data with standard terminologies in col 5, 267, 312
Replacing String in the columns with standard Terminology

5            direction
"Originating", "Outgoing"
"Terminating", "Incoming"

267          vpDialingfacResult
Success", "Voice Portal"

312          locationType
"Shared Call Appearance", "Secondary Device"
    
'''

print(raw_cdr_data[5])
print(raw_cdr_data[5].unique())

print(raw_cdr_data[267])
print(raw_cdr_data[267].unique())

print(raw_cdr_data[312])
print(raw_cdr_data[312].unique())


raw_cdr_data = replace_simple_with_Standard_terminology(raw_cdr_data)

print(raw_cdr_data[5].unique())
 
print(raw_cdr_data[267].unique())

print(raw_cdr_data[312].unique())




# 312 should have Primary and Secondary Device only

print(raw_cdr_data[312].unique())

raw_cdr_data[312] = remove_Unwanted_data(raw_cdr_data[312].tolist())

print(raw_cdr_data[312].unique())



print(raw_cdr_data[147])
# Is the 147 column has missing data, then create the data from 312 and 267
raw_cdr_data[147] = combine_All_Services(raw_cdr_data[147].tolist(),
                                             raw_cdr_data[312].tolist(),
                                             raw_cdr_data[267].tolist())
    
print(raw_cdr_data[147])




# we have made temporary 2 columns to find duration

raw_cdr_data["starttime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[9].tolist()))
print(raw_cdr_data["starttime"])
# 2019-06-25 19:21:43

raw_cdr_data["endtime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[13].tolist()))
print(raw_cdr_data["endtime"])
# 2019-06-25 19:24:54

raw_cdr_data["duration"] =  (raw_cdr_data["endtime"] - raw_cdr_data["starttime"]).astype("timedelta64[m]")
print(raw_cdr_data["duration"])
    

# use the new columns created time and date
# Creates 1 hour range for 24 hours
raw_cdr_data["hourly_range"] = hourly_range(raw_cdr_data["time"].tolist())
print(raw_cdr_data["hourly_range"])
# 19:00 - 19:59


# Creates similary in Week ( Monday to Sunday )
raw_cdr_data["weekly_range"] = weekly_range(raw_cdr_data["date"].tolist())
print(raw_cdr_data["weekly_range"])
# Tuesday

# Remove columns not required
raw_cdr_data = raw_cdr_data.drop("time", axis=1)
    
# Save the transformed data in CSV format for further use
raw_cdr_data.to_csv("cdr_data.csv", index = None)