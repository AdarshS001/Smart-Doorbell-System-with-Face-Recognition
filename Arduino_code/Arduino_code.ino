#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Airtel_9940040179";   // WiFi SSID
const char* password = "air18305";        // WiFi Password

WebServer server(80);

String receivedData = "";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nConnected to WiFi!");
    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
    server.handleClient();  // Handle web server requests

    if (Serial.available()) {
        receivedData = Serial.readStringUntil('\n');  // Read data until newline
        receivedData.trim();  // Remove extra spaces/newlines
        
        Serial.println("Received from Python: " + receivedData);  

        if (receivedData == "known") {
            Serial.println("✅ Face recognized! Please scan your RFID.");
            waitForRFID(); // Call function to wait for RFID
        } 
        else if (receivedData == "unknown") {
            Serial.println("❌ Warning! Unauthorized person detected!");
        } 
        else {
            Serial.println("⚠ Unexpected data received: [" + receivedData + "]");
        }
    }
}

// Function to simulate RFID scanning
void waitForRFID() {
    String rfidTag = "e3de15e";  // Fixed RFID Tag
    Serial.println("Waiting for RFID scan...");

    long startTime = millis();
    while (millis() - startTime < 10000) {  // Wait max 10 sec
        if (Serial.available()) {
            String scannedRFID = Serial.readStringUntil('\n');
            scannedRFID.trim();

            if (scannedRFID == rfidTag) {
                Serial.println("✅ RFID Matched! Access Granted.");
                return;
            } else {
                Serial.println("❌ Incorrect RFID! Try again.");
            }
        }
    }
    Serial.println("⏳ RFID scan timeout. Access Denied.");
}
