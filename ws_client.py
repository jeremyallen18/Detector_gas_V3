import asyncio
import websockets
import json
from mailer import enviar_correo

correo_enviado = False


async def conectar_ws(esp_ip, callback_ui):
    global correo_enviado

    uri = f"ws://{esp_ip}:81"
    callback_ui(f"Conectando a {uri}...\n")

    try:
        async with websockets.connect(uri) as ws:
            callback_ui("✔ Conectado\n")

            while True:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)

                    ao = data["AO"]
                    do = data["DO"]
                    alarma = data["alarma"]

                    callback_ui(f"AO={ao}   DO={do}   ALARMA={alarma}\n")

                    if alarma and not correo_enviado:
                        r = enviar_correo(ao, do)
                        callback_ui(r + "\n")
                        correo_enviado = True

                    elif not alarma:
                        correo_enviado = False

                except Exception as e:
                    callback_ui(f"Error en comunicación: {e}\n")
                    break

    except Exception as e:
        callback_ui(f"❌ No se pudo conectar: {e}\n")
