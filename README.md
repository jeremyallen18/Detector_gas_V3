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

## Base de datos MySQL

El sistema utiliza una base de datos MySQL para almacenar registros de lecturas y eventos de alarma.

### Requisitos

* MySQL Server (8.0 recomendado)
* MySQL Workbench o acceso por terminal
* Credenciales de un usuario con permisos de creación

---

### Creación de la base de datos

1. Abre MySQL Workbench o la terminal de MySQL.
2. Ejecuta el script SQL incluido en el proyecto:

```sql
-- Contenido ubicado en el archivo db.txt
```

Puedes hacerlo de dos formas:

**Desde MySQL Workbench**

* Archivo → Abrir Script SQL
* Selecciona `db.txt`
* Ejecuta el script completo

**Desde la terminal**

```bash
mysql -u usuario -p < db.txt
```

Este archivo crea la base de datos, tablas necesarias y su estructura inicial.

---

### Configuración de conexión (database.py)

El cliente Python obtiene la configuración de conexión desde el archivo `database.py`.

Antes de ejecutar el sistema, verifica y ajusta los siguientes parámetros:

```python
DB_HOST = "localhost"
DB_USER = "usuario"
DB_PASSWORD = "password"
DB_NAME = "detector_gas"
DB_PORT = 3306
```

**Importante:**
El valor de `DB_PORT` debe coincidir con el puerto configurado en el servidor MySQL del cliente.
Si tu MySQL usa un puerto distinto (ej. `3307`, `3308`), cámbialo aquí.

---

### Verificación de la base de datos

Para comprobar que la base de datos fue creada correctamente:

```sql
SHOW DATABASES;
USE detector_gas;
SHOW TABLES;
```

Si las tablas aparecen listadas, la base de datos está lista para usarse.

---

### Funcionamiento con la base de datos

* Cada lectura puede ser almacenada en MySQL
* Los eventos de alarma se registran para auditoría
* El sistema permite análisis posterior y generación de reportes

---

## Autor

**Jeremy Narvaez**
Proyecto escolar
Detector de Gas V3

