#!/bin/bash

# Instalar dependencias
pip3 install -r requirements.txt

# Ejecutar la aplicación con parámetros predeterminados
python3 weather_report.py --location "New York" --format "json"

# Ejecutar pruebas
python3 -m pytest tests/