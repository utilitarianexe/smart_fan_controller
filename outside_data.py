import datetime

import requests
import forecastio

import keys
import config

class OutsideData():
    def __init__(self):
        self.cached_temp = 70
        self.time_of_last_request = None
        self.minutes_5 = datetime.timedelta(minutes=config.temp_cache_frequency_minutes)
        
    def get_outside_temp(self, lat, lon):
        current_time = datetime.datetime.utcnow()
        if self.time_of_last_request is not None:
            time_from_last_request = current_time - self.time_of_last_request
            if time_from_last_request < self.minutes_5:
                return self.cached_temp, None

        try:
            temp = self.get_forecast_io_temp(lat, lon)
        except:
            error = 'failure of weather api this will probably resolve itself using last known outside temp'
            return self.cached_temp, error


        self.cached_temp = temp
        self.time_of_last_request = current_time
        return temp, None

    def get_forecast_io_temp(self, lat, lon):
        forecast = forecastio.load_forecast(keys.dark_sky_key, lat, lon)
        temp = forecast.currently().temperature
        return temp


    def get_open_weather_temp(lat, lon):
        uri = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'lat': lat, 'lon': lon, 'APPID':keys.open_weather_key}
        result = requests.get(uri, params=params)
        if result.status_code != 200:
            print(result.status_code)
        else:
            results = result.json()
            temp_k = result.json()['main']['temp']
            temp_f = (temp_k - 273.15) * 1.8 + 32.0
        return temp_f

outside_data = OutsideData()

