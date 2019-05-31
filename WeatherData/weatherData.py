import numpy as np
import matplotlib.pyplot as plt
import math, os, datetime, requests, sys
import pandas as pd

mytoken = 'ENxclfzjmtyBkmsDqOUGLcsXeYFbwHCC'

def get_filename(prefix, suffix, base_path):
    '''
    Gets a unique file name in the base path.
    
    Appends date and time information to file name and adds a number
    if the file name is stil not unique.
    prefix = Homework assignment name
    suffix = Extension
    base_path = Location of log file
    '''
    # Set base filename for compare
    fileNameBase = base_path + prefix + "_" + datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    # Set base for numbering system if filename exists
    num = 1
    # Generate complete filename to check existence
    fileName = fileNameBase + suffix
    # Find a unique filename
    while os.path.isfile(fileName):
        # if the filename is not unique, add a number to the end of it
        fileName = fileNameBase + "_" + str(num) + suffix
        # increments the number in case the filename is still not unique
        num = num + 1
    return fileName

lastyear = datetime.datetime.now()-datetime.timedelta(days=3650)
begin_date = lastyear.strftime("%Y-%m-%d")
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

locationid = 'WBAN13988' #location id for Independence
datasetid = 'LCD' #datset id for "Daily Summaries"

base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
base_url_stations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'

def get_weather(locationid, datasetid, begin_date, end_date, mytoken, base_url):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datasetid='+str(datasetid)+'&'+'locationid='+str(locationid)+'&'+'startdate='+str(begin_date)+'&'+'enddate='+str(end_date)+'&'+'limit=25'+'&'+'units=standard'
    
    r = requests.get(base_url, params = params, headers=token)
    print("Request status code: "+str(r.status_code))

    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved "+str(len(df['station'].unique()))+" stations")
        dates = pd.to_datetime(df['date'])
        print("Last date retrieved: "+str(dates.iloc[-1]))

        return df

    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting weather data to dataframe. Missing data?")

def get_station_info(locationid, datasetid, mytoken, base_url):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    
    stations = 'locationid='+str(locationid)+'&'+'datasetid='+str(datasetid)+'&'+'units=standard'+'&'+'limit=1000'
    r = requests.get(base_url, headers = token, params=stations)
    print("Request status code: "+str(r.status_code))

    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved "+str(len(df['id'].unique()))+" stations")
        
        if df.count().max() >= 1000:
            print('WARNING: Maximum data limit was reached (limit = 1000)')
            print('Consider breaking your request into smaller pieces')
 
        return df
    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting station data to dataframe. Missing data?")



df_weather = get_weather(locationid, datasetid, begin_date, end_date, mytoken, base_url_data)

df_stations = get_station_info(locationid, datasetid, mytoken, base_url_stations)

df_weather.head()

df_stations.head()

# df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')

# #Check for missing overlap between station weather info and location info
    
# location_ismissing = df_weather[~df_weather['station'].isin(df_stations['id'])]
# loc_miss_count = len(location_ismissing['station'].unique())
# if loc_miss_count != 0:
#     print("Missing location data for "+str(loc_miss_count)+" stations")
# else:
#     print("Successfully retrieved and combined location data")

# df.head()

# df.drop('id', inplace=True, axis=1)

# df.drop(['maxdate','mindate'],inplace=True,axis=1)

# df.to_csv('weather_'+str(begin_date)+'_noaa.csv', encoding='utf-8', index=False)