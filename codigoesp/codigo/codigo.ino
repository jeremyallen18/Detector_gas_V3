#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

const char* ssid = "COORDINACION INGLES 2.4G";
const char* password = "Mind3_1998@65";

WebSocketsServer webSocket(81);

// Pines
const int pinAO = 34;
const int pinDO = 14;
const int buzzer = 27;

// Variables para el sonido
bool tonoAlto = false; 
const int FREQ_ALTA = 2800; // Tono agudo penetrante
const int FREQ_BAJA = 1500; // Tono grave de alerta

// Variables de tiempo
unsigned long tiempoAnteriorAlarma = 0;
unsigned long tiempoAnteriorSocket = 0;
const unsigned long intervaloSocket = 300; // Enviar datos cada 300ms

// Estados
bool clienteConectado = false;

void setup() {
  Serial.begin(115200);
  pinMode(pinDO, INPUT);

  // Configuración ESP32
  ledcAttach(buzzer, 2000, 8); 

  // WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado a WiFi");
  Serial.println(WiFi.localIP());

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();
  
  // Configuracion para que funcione aun sin cliente conectado
  if (!clienteConectado) {
     verificarSensoresYAlarma(false); 
     return;
  }

  verificarSensoresYAlarma(true);
}

void verificarSensoresYAlarma(bool enviarDatos) {
  unsigned long ahora = millis();
  
  int valorAO = analogRead(pinAO);
  int valorDO = digitalRead(pinDO);
  bool alarma = false;

  // Lógica de activación
  if (valorAO > 1800 || valorDO == HIGH) {
    alarma = true;
    manejarAlarmaPro(valorAO);
  } else {
    ledcWriteTone(buzzer, 0); // Silencio
    tonoAlto = false;         // Resetear estado
  }

  // Enviar datos por WebSocket sin usar delay()
  if (enviarDatos && (ahora - tiempoAnteriorSocket >= intervaloSocket)) {
    tiempoAnteriorSocket = ahora;

    StaticJsonDocument<200> doc;
    doc["AO"] = valorAO;
    doc["DO"] = valorDO;
    doc["alarma"] = alarma;

    String payload;
    serializeJson(doc, payload);
    webSocket.broadcastTXT(payload);
  }
}

// Logica de alarma
void manejarAlarmaPro(int nivelGas) {
  unsigned long ahora = millis();

  // Mapear la velocidad de alternancia según el nivel de gas.
  // Poco gas (1800) = Cambia cada 600ms (lento, aviso).
  // Mucho gas (4095) = Cambia cada 100ms (muy rápido, pánico).
  int velocidadCambio = map(nivelGas, 1800, 4095, 600, 100);
  velocidadCambio = constrain(velocidadCambio, 100, 600);

  if (ahora - tiempoAnteriorAlarma >= velocidadCambio) {
    tiempoAnteriorAlarma = ahora;
    
    // Alternar entre tono alto y bajo
    tonoAlto = !tonoAlto;
    
    if (tonoAlto) {
      ledcWriteTone(buzzer, FREQ_ALTA);
    } else {
      ledcWriteTone(buzzer, FREQ_BAJA);
    }
  }
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED) {
    clienteConectado = true;
    Serial.println("Cliente conectado");
  }

  if (type == WStype_DISCONNECTED) {
    clienteConectado = false;
    Serial.println("Cliente desconectado");
    ledcWriteTone(buzzer, 0); // Asegurar silencio al desconectar
  }
}

//CONEXIONES: VIN: VCC, GND: GND, D14: D0, D34: A0
// BUZZER: D27:+, GND: -
