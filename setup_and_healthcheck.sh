#!/bin/bash

# Instalar dependencias
pip3 install -r requirements.txt

# Ejecutar la aplicación con parámetros predeterminados
py weather_report.py --location "New York" --format "json"

# Ejecutar pruebas
py -m pytest tests/