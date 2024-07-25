import serial
import requests

# Configure the serial port and baud rate (ensure it matches your Arduino setup)
serial_port = '/dev/ttyUSB0'  # Use the port identified in your test script
baud_rate = 9600

# Configure your Django server URL
server_url = 'http://127.0.0.1:8000/api/rfid'

def main():
    try:
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud rate.")
    except Exception as e:
        print(f"Failed to connect to serial port: {e}")
        return
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received: {line}")
            if line.startswith("ID:"):
                # Extract scanner ID and UID
                parts = line.split(',')
                scanner_id = parts[0].split(':')[1]
                uid = parts[1].split(':')[1]
                data = {'scanner_id': scanner_id, 'uid': uid}
                
                # Send data to Django backend
                try:
                    response = requests.post(server_url, json=data)
                    if response.status_code == 200:
                        print(f"Data sent successfully: {data}")
                    else:
                        print(f"Failed to send data: {response.status_code}, {response.text}")
                except Exception as e:
                    print(f"Error sending data to server: {e}")

if __name__ == '__main__':
    main()
