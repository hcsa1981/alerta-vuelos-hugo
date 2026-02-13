import requests
import smtplib
import os
import json
from datetime import datetime

# ==========================
# CONFIGURACIÓN
# ==========================

EMAIL = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

MAX_PRICE = 5000  # MXN por persona
ORIGIN = "MEX"
DESTINATION = "ORD"
ADULTS = 2
CHILDREN = 1

FECHAS_IDA = ["23/07/2026", "24/07/2026", "25/07/2026"]
FECHAS_REGRESO = ["06/08/2026", "07/08/2026", "08/08/2026"]

PRICE_FILE = "precio_guardado.json"

# ==========================
# FUNCIÓN PARA OBTENER PRECIO
# ==========================

def buscar_precio():
    mejor_precio = None

    for ida in FECHAS_IDA:
        for vuelta in FECHAS_REGRESO:
            url = f"https://api.tequila.kiwi.com/v2/search"
            headers = {
                "apikey": os.environ.get("KIWI_API")
            }
            params = {
                "fly_from": ORIGIN,
                "fly_to": DESTINATION,
                "date_from": ida,
                "date_to": ida,
                "return_from": vuelta,
                "return_to": vuelta,
                "adults": ADULTS,
                "children": CHILDREN,
                "curr": "MXN",
                "max_stopovers": 0
            }

            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            if "data" in data and len(data["data"]) > 0:
                precio = data["data"][0]["price"]
                if mejor_precio is None or precio < mejor_precio:
                    mejor_precio = precio

    return mejor_precio


# ==========================
# EMAIL
# ==========================

def enviar_correo(precio):
    subject = f"ALERTA ✈️ Precio bajo encontrado: ${precio} MXN"
    body = f"""
Se encontró un mejor precio.

Precio total detectado: ${precio} MXN
Ruta: MEX → ORD
Fechas: 23–25 julio / 6–8 agosto 2026
Aeroméxico
Sin escalas

Fecha de detección: {datetime.now()}
"""

    mensaje = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.sendmail(EMAIL, EMAIL, mensaje)
    server.quit()


# ==========================
# LÓGICA PRINCIPAL
# ==========================

def cargar_precio_anterior():
    try:
        with open(PRICE_FILE, "r") as f:
            return json.load(f)["precio"]
    except:
        return None


def guardar_precio(precio):
    with open(PRICE_FILE, "w") as f:
        json.dump({"precio": precio}, f)


if __name__ == "__main__":
    precio_actual = buscar_precio()
    precio_anterior = cargar_precio_anterior()

    if precio_actual:
        print("Precio actual:", precio_actual)

        if (
            precio_anterior is None
            or precio_actual < precio_anterior
            or (precio_actual / 3) <= MAX_PRICE
        ):
            enviar_correo(precio_actual)
            guardar_precio(precio_actual)
            print("Correo enviado.")
        else:
            print("No hay mejora de precio.")
