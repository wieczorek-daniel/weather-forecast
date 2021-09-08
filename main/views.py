from django.shortcuts import render
import urllib.request
import json
from datetime import datetime
from weather_forecast.settings import OPENWEATHERMAP_API_KEY


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        request_url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid='+OPENWEATHERMAP_API_KEY
        data_source = urllib.request.urlopen(request_url).read()
        api_data = json.loads(data_source)

        data = {
            "country_code": api_data['sys']['country'],
            "country_name": api_data['name'],
            "latitude": api_data['coord']['lat'],
            "longitude": api_data['coord']['lon'],
            "temperature": str(api_data['main']['temp'])+f'\N{DEGREE SIGN}C',
            "pressure": str(api_data['main']['pressure'])+'hPa',
            "humidity": str(api_data['main']['humidity'])+'%',
            "main_information": api_data['weather'][0]['main'],
            "description": api_data['weather'][0]['description'],
            "icon": api_data['weather'][0]['icon'],
            "current_time": f"{datetime.utcfromtimestamp(api_data['dt']+api_data['timezone']):%Y-%m-%d %I:%M %p}",
            "sunrise": f"{datetime.utcfromtimestamp(api_data['sys']['sunrise']+api_data['timezone']):%Y-%m-%d %I:%M %p}",
            "sunset": f"{datetime.utcfromtimestamp(api_data['sys']['sunset']+api_data['timezone']):%Y-%m-%d %I:%M %p}",
        }
    else:
        data = {}

    return render(request, "main/index.html", data)
