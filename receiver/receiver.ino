#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_PIN          10         // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

const char* scannerID = "Scanner_1"; // Unique identifier for this scanner

void setup() {
    Serial.begin(9600);            // Initialize serial communications with the PC
    while (!Serial);               // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
    SPI.begin();                   // Init SPI bus
    mfrc522.PCD_Init();            // Init MFRC522
    delay(4);                      // Optional delay. Some boards need more time after init to be ready
    Serial.println(F("Scan PICC to see UID..."));
}

void loop() {
    // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
    if (!mfrc522.PICC_IsNewCardPresent()) {
        return;
    }

    // Select one of the cards
    if (!mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    // Display scanner ID and UID on Serial Monitor
    Serial.print(F("Scanner ID: "));
    Serial.print(scannerID);
    Serial.print(F(" - Card UID:"));
    String uidStr = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
        uidStr += String(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println();

    // Send data to computer via serial
    Serial.print("ID:");
    Serial.print(scannerID);
    Serial.print(",UID:");
    Serial.println(uidStr);

    // Halt PICC
    mfrc522.PICC_HaltA();
}
