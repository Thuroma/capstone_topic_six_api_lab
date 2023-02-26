"""
This program is a weather app that allows users to view a five day forecast for a selected city.
The user enters the name of a city with the country code
The application displays each of these in three hour increments for the next five days:
- temperature (F)
- timestamp
- weather description
- wind speed
The timestamp is displayed in local time for readability
Logging is used to document all system problems as well as show when a new query was made
The logged information for this program is in lab.log
Printing is used to alert the user when something prevents a forecast from being retrieved
"""


from datetime import datetime, date, time
import requests
import logging
import os


#   Set up the file for the program log and set the lowest level to record as DEBUG
logging.basicConfig(filename='lab.log', level=logging.INFO, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#   API base URL and key (environment variable)
url = 'http://api.openweathermap.org/data/2.5/forecast'
key = os.environ.get('WEATHER_KEY')


""" 
The main function, sends for forecast information and sends that information to be printed 
"""
def main():
    location = get_location()
    weather_data, error = get_forecast(location, key)
    if error:
        print('Sorry, could not get the weather.')
    else:
        logging.info(f'The user requested a forecast from the API.')
        build_periodic_forecast(weather_data)
            

""" 
This function retrieves the location data from the forecast
It saves the city and state to be used in the params for the API call
Returns 'str,str'
"""
def get_location():
    city, country = '', ''
    while len(city) == 0:
        city = input('Enter the name of a city: ').strip()

    while len(country) != 2 or not country.isalpha():
        country = input('Enter the two digit country code for your city: ').strip()

    location = f'{city},{country}'
    return location


""" 
This function uses the 'city,country code' to get the forecast for the selected location
The returned data is converted to json
The list containing the 5 day forecast is returned along with any errors
"""
def get_forecast(location,key):
    try:
        query = {'q': location, 'units': 'imperial', 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status() # Raise exception for 400 or 500 errors
        data = response.json()
        forecast_data = data['list']
        return forecast_data, None
    except Exception as e:
        logging.exception(f'There was an issue retrieving the forecast from the API: {e}')
        return None, e
    

""" 
This function consolidates the individual weather data values then 
sends them to be printed to the user
"""
def build_periodic_forecast(weather_data):
    for forecast in weather_data:
            temp = get_temp(forecast)
            timestamp = get_timestamp(forecast)
            weather_description = get_weather_description(forecast)
            wind_speed = get_wind_speed(forecast)
            print_forecast(temp, timestamp, weather_description, wind_speed)


""" 
This function gets and returns the temperature from the forecast
"""
def get_temp(weather_data):
    try:
        temp = weather_data['main']['temp']
        return temp
    except Exception as e:
        logging.exception(f'There was an error retrieving the temperature from the API: {e}')
        return 'Unknown'


""" 
This function gets and returns the formatted timestamp from the forecast
"""   
def get_timestamp(weather_data):
    try:
        timestamp = weather_data['dt']
        forecast_date = datetime.fromtimestamp(timestamp)
        forecast_date_time = forecast_date.strftime("%A %B %d, %Y at %I:%M%p")
        return forecast_date_time
    except ValueError as e:
        logging.exception(f'Response received from datetime exception while retrieving timestamp: {e}')
        return 'Unknown'


""" 
This function gets and returns the weather description from the forecast
"""    
def get_weather_description(weather_data):
    try:
        weather_description = weather_data['weather'][0]['description']
        return weather_description
    except Exception as e:
        logging.exception(f'There was an error retrieving the weather description from the API: {e}')
        return 'Unknown'


""" 
This function gets and returns the wind speed from the forecast
"""  
def get_wind_speed(weather_data):
    try:
        wind_speed = weather_data['wind']['speed']
        return wind_speed
    except Exception as e:
        logging.exception(f'There was an error retrieving the wind speed from the API: {e}')
        return 'Unknown'
    

""" 
This function uses the individual weather data values from build_periodic_forecast
then prints a formatted string for the user
"""
def print_forecast(temp, timestamp, weather_description, wind_speed):
    print(f'The temperature will be {temp}F on {timestamp}. \n'
          f'The forecast predicts {weather_description} with winds of {wind_speed}mph.\n')


if __name__ == '__main__':
    main()