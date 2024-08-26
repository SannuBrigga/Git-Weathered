import requests
import argparse
import json
import csv

URL = "https://api.weatherapi.com/v1/current.json"
# Make this via env variable
API_KEY = "d9432060466a4f4a83563950242308"

def save_to_json(filename, data):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file)
    
    print("Datos almacenados en formato JSON con éxito...")

def save_to_txt(filename, data):
    file_data = ""
    # Parse the raw report data
    for location_report in data:
        file_data += f"# {location_report['location']}\n"
        file_data += f"# {location_report['country']}\n"
        file_data += f"- Condición climática: {location_report['condition']}\n"
        file_data += f"- Temperatura: {location_report['temperature']}\n"
        file_data += f"- Dirección del viento: {location_report['wind_direction']}\n"
        file_data += f"- Humedad: {location_report['humidity']}\n"
        file_data += f"- Sensación Térmica: {location_report['feels_like']}\n"

        file_data += f"{''.join(['-'] * 32)}\n"

    with open(f"{filename}.txt", "w") as file:
        file.write(file_data)

    print("Datos almacenados en formato TXT con éxito...")

def save_to_csv(filename, data):
    csv.register_dialect('custom_dialect', delimiter='|')

    with open(f"{filename}.csv", "w") as file:
        writer = csv.DictWriter(file, dialect='custom_dialect', fieldnames=data[0].keys())
        writer.writeheader()

        for record in data:
            writer.writerow(record)
    
    print("Datos almacenados en formato CSV con éxito...")

Storage = {
    'json': save_to_json,
    'csv': save_to_csv,
    'txt': save_to_txt,
}

def cli_parser():
    parser = argparse.ArgumentParser(description="App CLI de consulta del clima")
    parser.add_argument("-l", "--location", required=True, nargs="+", help="La localidad que desea consultar. Ej: Ciudad del Este - Paraguay")
    parser.add_argument("-f", "--format", default=["txt"], nargs="+", choices=['json', 'csv', 'txt'], help="Formato en el cuál desea obtener los datos. Ej: json, txt, csv")

    return parser.parse_args()

def get_weather_data(location):
    payload = {
        "q": location,
        "lang": "es",
        "key": API_KEY
    }

    try:
        response = requests.get(URL, params=payload)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return {
            "error": "Ocurrió un error al buscar la ubicación"
        }

    response_json = response.json()

    if response_json.get('error'):
        if response_json['error']['code'] == 1006:
            return {
                "error": "No se encontró la ciudad ingresada"
            }

    return {
        'location': response_json['location']['name'],
        'country': response_json['location']['country'],
        'condition': response_json['current']['condition']['text'],
        'temperature': response_json['current']['temp_c'],
        'wind_direction': response_json['current']['wind_dir'],
        'wind_speed': response_json['current']['wind_kph'],
        'humidity': response_json['current']['humidity'],
        'feels_like': response_json['current']['feelslike_c']
    }


def main():
    args = cli_parser()

    weather_report = []

    # Parse the location
    if args.location:
        for location in args.location:
            location_report = get_weather_data(location)
            if location_report.get("error"):
                print(location_report["error"])
                return

            weather_report.append(location_report)

    # Parse the data to the formats
    for storage_format in args.format:
        Storage[storage_format]("weather_report", weather_report)

if __name__ == "__main__":
    main()