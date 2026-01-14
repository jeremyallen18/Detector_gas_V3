import asyncio
import websockets
import json
import re
from mailer import enviar_correo

correo_enviado = False


def validar_ip(ip):
    """Valida formato de dirección IP"""
    patron = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(patron, ip):
        octetos = ip.split('.')
        return all(0 <= int(octeto) <= 255 for octeto in octetos)
    return False


async def conectar_ws(esp_ip, callback_ui):
    global correo_enviado

    # Validar IP antes de conectar
    if not validar_ip(esp_ip):
        callback_ui(f"❌ IP inválida: {esp_ip}\n")
        return

    uri = f"ws://{esp_ip}:81"
    callback_ui(f"Conectando a {uri}...\n")

    try:
        # Agregar timeout para la conexión
        async with websockets.connect(
            uri,
            ping_interval=20,
            ping_timeout=10,
            close_timeout=10
        ) as ws:
            callback_ui("✔ Conectado\n")

            while True:
                try:
                    # Agregar timeout para recepción de mensajes
                    msg = await asyncio.wait_for(ws.recv(), timeout=30)
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

                except asyncio.TimeoutError:
                    callback_ui("⚠ Timeout esperando datos del ESP32\n")
                    break
                except json.JSONDecodeError as e:
                    callback_ui(f"⚠ Error decodificando JSON: {e}\n")
                except KeyError as e:
                    callback_ui(f"⚠ Dato faltante en mensaje: {e}\n")
                except Exception as e:
                    callback_ui(f"Error en comunicación: {e}\n")
                    break

    except asyncio.TimeoutError:
        callback_ui(f"❌ Timeout al conectar a {uri}\n")
    except ConnectionRefusedError:
        callback_ui(f"❌ Conexión rechazada. Verifica que el ESP32 esté activo en {esp_ip}\n")
    except OSError as e:
        callback_ui(f"❌ Error de red: {e}\n")
    except Exception as e:
        callback_ui(f"❌ No se pudo conectar: {e}\n")