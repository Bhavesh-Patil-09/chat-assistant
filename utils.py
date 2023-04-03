import requests
from geopy.geocoders import MapQuest
from geopy import distance
import random


def get_weather_condition(key, city):
    try:
        weather_key = key
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=params)
        weather = response.json()
        print(weather)
        text = "The weather condition of " + str(weather['name']) + " is as follows " + "the overhead condition is " + \
            str(weather['weather'][0]['description']) + " and the temperature in fahrenheit is " + str(weather['main']['temp'])
        return text
    except:
        return "Oops! Could not find any city by this name"


def get_news_headline(key):
    # Return headlines of top news

    # Replace YOUR_API_KEY with your actual API key
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={key}'

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Retrieve the top news from the response JSON
        top_news = response.json()['articles']

        # Print the headlines and descriptions of the top news
        # for news in top_news:
        #     print(news['title'])
        #     print(news['description'])
        #     print()
        return top_news[0]['title']
    else:
        return None
    

def get_location_coordinates(key, place):

    '''
        Note that this method may not always be accurate, as your IP address may be assigned to a different location
        than your physical location. Additionally, some ISPs may use dynamic IP addresses, which may change over time.
        For more accurate location information, you may need to use a different method such as GPS or Wi-Fi triangulation.

        crosscheck --> https://ipstack.com/ ->( here ip is your public ip can be verified by typing get my ip) 
    '''
    # create a geolocator object with the MapQuest
    geolocator = MapQuest(key)

    # get the location information using the IP address
    location = geolocator.geocode(place)
    return (location.latitude, location.longitude)
    

def get_distance(key, place1: str, place2: str):
    # Return distance in kilometers
    try:
        if all([place1, place2]):
            dist = round(distance.distance(place1, place2).km, 1)
            print(dist)
            return dist
        else:
            dist = round(random.random(), 1)
    except Exception as e:
        dist = round(random.random(), 1)
        return dist