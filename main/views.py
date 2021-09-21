from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import folium
from branca.element import Figure
from datetime import datetime
from weather_forecast.settings import OPENWEATHERMAP_API_KEY


def index(request):
    if request.method == 'POST':
        city = urllib.parse.quote_plus(request.POST['city'])
        request_url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid='+OPENWEATHERMAP_API_KEY
        try:
            data_source = urllib.request.urlopen(request_url).read()
            api_data = json.loads(data_source)

            figure = Figure(height="100%")
            map = folium.Map(location=[api_data['coord']['lat'], api_data['coord']['lon']], zoom_start=10)
            folium.Marker(
                location=[api_data['coord']['lat'], api_data['coord']['lon']],
                popup=api_data['name'],
                icon=folium.Icon(icon="cloud"),
            ).add_to(map)
            figure.add_child(map)

            data = {
                "country_code": api_data['sys']['country'],
                "country_name": api_data['name'],
                "latitude": api_data['coord']['lat'],
                "longitude": api_data['coord']['lon'],
                "temperature": str(api_data['main']['temp']) + f'\N{DEGREE SIGN}C',
                "pressure": str(api_data['main']['pressure']) + 'hPa',
                "humidity": str(api_data['main']['humidity']) + '%',
                "main_information": api_data['weather'][0]['main'],
                "description": api_data['weather'][0]['description'],
                "icon": api_data['weather'][0]['icon'],
                "current_time": f"{datetime.utcfromtimestamp(api_data['dt'] + api_data['timezone']):%Y-%m-%d %I:%M %p}",
                "sunrise": f"{datetime.utcfromtimestamp(api_data['sys']['sunrise'] + api_data['timezone']):%Y-%m-%d %I:%M %p}",
                "sunset": f"{datetime.utcfromtimestamp(api_data['sys']['sunset'] + api_data['timezone']):%Y-%m-%d %I:%M %p}",
                "map": figure._repr_html_(),
            }
        except urllib.error.HTTPError:
            data = {
                "error_occurred": True,
                "error_message": 'Can not find a city based on the entered text.',
            }
    else:
        data = {}

    return render(request, "main/index.html", data)


def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response
