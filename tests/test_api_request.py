import unittest
from unittest.mock import patch
from weather_report import get_weather_data

API_RESPONSE_JSON = {
    "location": {
        "name": "Ciudad Del Este",
        "region": "Alto Parana",
        "country": "Paraguay",
        "lat": -25.52,
        "lon": -54.62,
        "tz_id": "America/Asuncion",
        "localtime_epoch": 1724652299,
        "localtime": "2024-08-26 02:04"
    },
    "current": {
        "last_updated_epoch": 1724652000,
        "last_updated": "2024-08-26 02:00",
        "temp_c": 4.2,
        "temp_f": 39.6,
        "is_day": 0,
        "condition": {
        "text": "Despejado",
        "icon": "//cdn.weatherapi.com/weather/64x64/night/113.png",
        "code": 1000
        },
        "wind_mph": 2.2,
        "wind_kph": 3.6,
        "wind_degree": 10,
        "wind_dir": "N",
        "pressure_mb": 1028,
        "pressure_in": 30.36,
        "precip_mm": 0,
        "precip_in": 0,
        "humidity": 93,
        "cloud": 0,
        "feelslike_c": 2.9,
        "feelslike_f": 37.2,
        "windchill_c": 3.6,
        "windchill_f": 38.5,
        "heatindex_c": 4.8,
        "heatindex_f": 40.7,
        "dewpoint_c": 2.4,
        "dewpoint_f": 36.3,
        "vis_km": 10,
        "vis_miles": 6,
        "uv": 1,
        "gust_mph": 7.4,
        "gust_kph": 11.9
    }
}

class TestAPIRequest(unittest.TestCase):
    @patch("weather_report.requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = API_RESPONSE_JSON

        result = get_weather_data("Ciudad del Este")
        self.assertEqual(result, {
            'location': API_RESPONSE_JSON['location']['name'],
            'country': API_RESPONSE_JSON['location']['country'],
            'condition': API_RESPONSE_JSON['current']['condition']['text'],
            'temperature': API_RESPONSE_JSON['current']['temp_c'],
            'wind_direction': API_RESPONSE_JSON['current']['wind_dir'],
            'wind_speed': API_RESPONSE_JSON['current']['wind_kph'],
            'humidity': API_RESPONSE_JSON['current']['humidity'],
            'feels_like': API_RESPONSE_JSON['current']['feelslike_c']
        })
