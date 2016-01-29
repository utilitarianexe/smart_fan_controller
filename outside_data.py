import requests

def get_outside_temp(lat, lon):
    uri = 'http://api.openweathermap.org/data/2.5/weather'
    api_key = 'f427e209e3a947301615a4d8102cc548'
    params = {'lat': lat, 'lon': lon, 'APPID':api_key}
    result = requests.get(uri, params=params)
    if result.status_code != 200:
        print(result.status_code)
    else:
        results = result.json()
        temp_k = result.json()['main']['temp']
        temp_f = (temp_k - 273.15) * 1.8 + 32.0
    return temp_f
