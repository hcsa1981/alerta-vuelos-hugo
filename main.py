import requests
import smtplib
import os
import json
from datetime import datetime

# ==========================
# CONFIGURACIÓN
# ==========================

API_KEY = os.environ.get("AMADEUS_API_KEY")
API_SECRET = os.environ.get("AMADEUS_API_SECRET")

EMAIL = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

MAX_PRICE = 5000  # MXN por persona
ORIGIN = "MEX"
DESTINATION = "ORD"
ADULTS = 2
CHILDREN = 1

FECHAS_IDA = ["2026-07-23", "2026-07-24", "2026-07-25"]
FECHAS_REGRESO = ["2026-08-06", "2026-08-07", "2026-08-08"]

PRICE_FILE = "precio_guardado.json"

# ==========================
# TOKEN AMADEUS
# ==========================

def obtener_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET,
    }
    response = requests.post(url, data=data)
    return response.json()["access_token"]


# ==========================
# BUSCAR PRECIO
# ==========================

def buscar_precio():
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}
    mejor_precio = None

    for ida in FECHAS_IDA:
        for vuelta in FECHAS_REGRESO:

            params = {
                "originLocationCode": ORIGIN,
                "destinationLocationCode": DESTINATION,
                "departureDate": ida,
                "returnDate": vuelta,
                "adults": ADULTS,
                "children": CHILDREN,
                "cur
