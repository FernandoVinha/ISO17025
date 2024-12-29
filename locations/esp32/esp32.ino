#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// Configurações do Wi-Fi
const char* ssid = "VINHA";          // Substitua pelo SSID da sua rede Wi-Fi
const char* password = "Fhbkw8jd";  // Substitua pela senha da sua rede Wi-Fi
// URL do endpoint Django para criar medições
const char* serverName = "http://192.168.0.5:8000/locations/api/create-room-measurement/";

// Variável para armazenar a ID da sala
const int room_id = 1;  // Substitua pela ID correta da sala

// Configurações do sensor DHT11
#define DHTPIN 14        // Pino ao qual o DHT11 está conectado
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Configuração do LED embutido
#define LED_BUILTIN 25  // Confirme o pino correto para o seu ESP32 Heltec LoRa V2

// Variáveis para controle de tempo
unsigned long previousDHTMillis = 0;
const long dhtInterval = 1000;  // Intervalo para leitura do DHT11 (1 segundo)

// Variáveis para armazenar a última leitura do DHT11
float lastTemperature = NAN;
float lastHumidity = NAN;

void setup() {
  Serial.begin(115200);
  Serial.println("Inicializando...");

  pinMode(LED_BUILTIN, OUTPUT);  // Configura o LED embutido como saída

  dht.begin();  // Inicializa o sensor DHT11
  Serial.println("DHT11 inicializado.");

  // Conecta-se ao Wi-Fi
  connectToWiFi();
}

void loop() {
  unsigned long currentMillis = millis();

  // Reconecta ao Wi-Fi caso necessário
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  // Lê os dados do sensor DHT11 e envia ao servidor a cada 1 segundo
  if (currentMillis - previousDHTMillis >= dhtInterval) {
    previousDHTMillis = currentMillis;
    readAndSendDHTData();
  }
}

void connectToWiFi() {
  Serial.print("Conectando ao WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nConectado ao WiFi!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void readAndSendDHTData() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (!isnan(temperature) && !isnan(humidity)) {
    Serial.printf("Temperatura: %.2f °C\n", temperature);
    Serial.printf("Umidade: %.2f %%\n", humidity);

    // Envia os dados ao servidor
    sendToServer(temperature, humidity);
  } else {
    Serial.println("Falha ao ler o sensor DHT11! Verifique as conexões.");
  }
}

void sendToServer(float temperature, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);  // Define o URL do servidor
    http.addHeader("Content-Type", "application/json");  // Define o cabeçalho

    // Cria o JSON para enviar ao servidor
    String postData = "{\"room\": " + String(room_id) + 
                      ", \"temperature\": " + String(temperature, 2) + 
                      ", \"humidity\": " + String(humidity, 2) + "}";

    Serial.println("Enviando dados ao servidor: " + postData);

    // Faz a requisição POST
    int httpResponseCode = http.POST(postData);

    // Verifica a resposta
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Resposta do servidor: " + response);
    } else {
      Serial.print("Erro na solicitação HTTP: ");
      Serial.println(httpResponseCode);
    }

    http.end();  // Finaliza a conexão HTTP
  } else {
    Serial.println("Erro: Wi-Fi desconectado.");
  }
}
