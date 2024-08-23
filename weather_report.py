import requests
import argparse

url = "https://api.weatherapi.com/v1/current.json"
# Make this via env variable
API_KEY = "d9432060466a4f4a83563950242308"

def main():
    parser = argparse.ArgumentParser(description="App CLI de consulta del clima")
    parser.add_argument("-l", "--location", required=True, nargs="+", help="La localidad que desea consultar. Ej: Ciudad del Este - Paraguay")
    parser.add_argument("-f", "--format", default=["txt"], nargs="+", choices=['json', 'csv', 'txt'], help="Formato en el cuál desea obtener los datos. Ej: json, txt, csv")

    args = parser.parse_args()

    weather_report = []

    # Parse the location
    if args.location:
        for location in args.location:
            payload = {
                "q": location,
                "lang": "es",
                "key": API_KEY
            }

            response = requests.get(url, params=payload)

            response_json = response.json()

            location_report = {
                'location': response_json['location']['name'],
                'country': response_json['location']['country'],
                'condition': response_json['current']['condition']['text'],
                'temperature': response_json['current']['temp_c'],
                'wind_direction': response_json['current']['wind_dir'],
                'wind_speed': response_json['current']['wind_kph'],
                'humidity': response_json['current']['humidity'],
                'feels_like': response_json['current']['feelslike_c']
            }

            weather_report.append(location_report)

if __name__ == "__main__":
    main()