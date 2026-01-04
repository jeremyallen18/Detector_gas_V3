#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

const char* ssid = "FIBRA OPTICA NARVIZ";
const char* password = "DANA8112VAYA$";

WebSocketsServer webSocket = WebSocketsServer(81);

const int pinAO = 34;  // Entrada analógica
const int pinDO = 14;  // Entrada digital
const int buzzer = 27; // Buzzer activo

bool alarmaDisparada = false;
bool clienteConectado = false;

void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(pinDO, INPUT);
  pinMode(buzzer, OUTPUT);

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado a WiFi");
  Serial.print("IP asignada: ");
  Serial.println(WiFi.localIP());

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  Serial.println("WebSocket listo en puerto 81");
}

void loop() {
  webSocket.loop();

  if (!clienteConectado) return;

  int valorAO = analogRead(pinAO);
  int valorDO = digitalRead(pinDO);

  bool alarma = false;

  if ((valorDO == HIGH || valorAO > 2000) && !alarmaDisparada) {
    activarAlarma();
    alarmaDisparada = true;
    alarma = true;
  }

  if (valorDO == LOW && valorAO <= 1800) {
    alarmaDisparada = false;
  }

  StaticJsonDocument<200> doc;
  doc["AO"] = valorAO;
  doc["DO"] = valorDO;
  doc["alarma"] = alarma;

  String payload;
  serializeJson(doc, payload);

  webSocket.broadcastTXT(payload);
  delay(500);
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED) {
    clienteConectado = true;
    Serial.println("Cliente WebSocket conectado");
  }

  if (type == WStype_DISCONNECTED) {
    clienteConectado = false;
    Serial.println("Cliente WebSocket desconectado");
  }
}

void activarAlarma() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(buzzer, HIGH);
    delay(80);
    digitalWrite(buzzer, LOW);
    delay(80);
  }
}

//CONEXIONES: VIN: VCC, GND: GND, D14: D0, D34: A0
// BUZZER: D27:+, GND: -
