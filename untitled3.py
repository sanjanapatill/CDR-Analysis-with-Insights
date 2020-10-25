# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 19:34:38 2020

@author: Sanjana
"""

# https://pastebin.com/QbYwcrgh
""" 
This is the initial stage of the CDR Analysis project.
We are going to learn about loading the CDR data and transform it for our 
Data Analysis and visualization purpose for Business perspective.
"""

"""
   column no -  actual name
    1            serviceProvider
    4            group Information
    5            direction
    9            startTime
    13           EndTime
    14           Miss Call Information
    31           Group ID
    120          userId
    180          twoStageDialingDigits
    146          relatedCallId
    147          relatedCallIdReason
    267          vpDialingfacResult
    312          locationType
    345          userAgent
  
                 date
                 starttime
                 endtime
                 duration
                 hourly_range
                 weekly_range
"""   

# Loading all your libraries
import pandas as pd


# Declaring your Global variables


# main function to load the data and transform it for further use
def main():
    
    dataset_name =  "cdr_data.csv"
    
    # Required columns
    call_columns = ["4", "5","14", "31", "120", "147", "267", "312", "345", \
                    "date","starttime", "endtime","duration", "hourly_range","weekly_range"]
    
    # We have used low_memory = False as some columns contains mixed datatype
    # header =  None is used as dataset doesn't contain column name
    call_dataset = pd.read_csv(dataset_name, usecols = call_columns,low_memory = False)
        
    

    # coulmns for service data
    service_columns = ["31", "120", "147", "345","date", "starttime", "endtime","duration"]
    service_dataset = call_dataset[service_columns]
    
    
    # columns for device data
    device_columns = ["5", "31", "120", "312", "345", "date","starttime", "endtime","duration"]
    device_dataset = call_dataset[device_columns]
    
    
    
    # Output


    # Renaming columns name according to the Client
    
    call_dataset = call_dataset.rename(columns = {"4":"Group", "5":"Call_Direction","14":"Missed Calls",
                                            "31":"GroupID", "120":"UserID", "147":"Features", "267":" vpDialingfacResult",
                                            "312":"UsageDeviceType",
                                            "345":"UserDeviceType"})
    
    
    service_dataset = service_dataset.rename(columns={"120":"UserID", 
                                                  "31":"GroupID", "147":"FeatureName",
                                                  "345":"UserDeviceType","date":"FeatureEventDate"
                                                  })
    
    

    device_dataset = device_dataset.rename(columns={"5": "DeviceEventTypeDirection", 
                                      "120":"UserID", "31":"GroupID", 
                                      "345":"UserDeviceType","date":"DeviceEventDate", 
                                      "312":"UsageDeviceType"})

    
    
    
    call_dataset.to_csv("Call_data.csv", index=None)
    service_dataset.to_csv("Service_data.csv", index=None)
    device_dataset.to_csv("Device_data.csv", index=None)



if (__name__ == '__main__'):
    main()
    