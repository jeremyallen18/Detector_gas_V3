# Detector_gas_V3

Sistema de detección de gas basado en ESP32 + sensor MQ-2, con **alarma sonora**, **conectividad WiFi** y **comunicación WebSocket** para monitoreo en tiempo real desde una aplicación en Python.

---

## Descripción general

Este proyecto detecta la presencia de gas mediante un sensor MQ-2.
Cuando se supera un umbral crítico:

* Se activa una **alarma sonora**
* Se envían **lecturas en tiempo real** vía WebSocket
* Un cliente externo (Python) recibe los datos y puede ejecutar acciones como **envío de correos de alerta**

El ESP32 se conecta a una red WiFi y **solo comienza a enviar datos cuando un cliente se conecta**, evitando tráfico innecesario.

---

## Requisitos

### Hardware

* ESP32
* Sensor MQ-2
* Buzzer activo
* Protoboard
* Cables Dupont

### Software

* Arduino IDE
* Python 3.9 o superior
* Git
* Librerías Arduino:

  * WiFi (incluida con ESP32)
  * WebSocketsServer
  * ArduinoJson (v6)

### Librerías Python

```bash
pip install websockets
```

---

## Conexiones

### Sensor MQ-2

* VIN → VCC
* GND → GND
* D0 → GPIO 14
* A0 → GPIO 34

### Buzzer

* * → GPIO 27
* – → GND

---

## Configuración WiFi

En el archivo del firmware (`.ino`), edita:

```cpp
const char* ssid = "TU_RED_WIFI";
const char* password = "TU_PASSWORD";
```

---

## Funcionamiento del sistema

1. El ESP32 se conecta a la red WiFi
2. Obtiene una **IP local**
3. Inicia un **servidor WebSocket en el puerto 81**
4. Espera a que un cliente se conecte
5. Al conectarse el cliente:

   * Se comienzan a enviar lecturas en formato JSON
6. Si se detecta gas:

   * Se activa la alarma una sola vez por evento
   * Se notifica al cliente

---

## Formato de datos enviados (JSON)

```json
{
  "AO": 2150,
  "DO": 1,
  "alarma": true
}
```

* `AO`: Lectura analógica del sensor
* `DO`: Estado digital del sensor
* `alarma`: Indica si la alarma fue activada

---

## Cliente Python

El cliente Python se conecta mediante WebSocket usando la IP del ESP32:

```python
ws://IP_DEL_ESP32:81
```

Una vez conectado:

* Recibe lecturas en tiempo real
* Detecta eventos de alarma
* Puede ejecutar acciones automáticas (ej. envío de correos)

---

## Ejecución del cliente Python

```bash
python main.py
```

Asegúrate de que:

* El ESP32 esté encendido
* Ambos dispositivos estén en la **misma red**
* La IP del ESP32 sea correcta

---

## Consideraciones importantes

* El sistema **no envía datos si no hay cliente conectado**
* La alarma no se reproduce en bucle
* El umbral analógico puede ajustarse en el código
* Se recomienda calibrar el sensor MQ-2 antes de uso real

---

## Autor

**Jeremy Allen**
Proyecto académico / experimental
Detector de Gas V3

