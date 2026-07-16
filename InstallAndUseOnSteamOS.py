#####
'''
# Disable SteamOS read-only mode to allow system changes
sudo steamos-readonly disable

# Initialize the package manager's keyring
sudo pacman-key --init

# Add Holo repository keys to the keyring
sudo pacman-key --populate holo

# Update all system packages to the latest versions
sudo pacman -Syu

# Install Mosquitto MQTT broker package
sudo pacman -S mosquitto

# Start Mosquitto and display verbose output
mosquitto -v

## CTRL+X to exit the verbose output

# Create the configuration directory for Mosquitto
mkdir -p ~/.config/mosquitto

# Edit the Mosquitto configuration file
nano ~/.config/mosquitto/mosquitto.conf

# Enable Mosquitto to start automatically on boot
sudo systemctl enable mosquitto.service

# Start the Mosquitto service immediately
sudo systemctl start mosquitto.service

# Check if the Mosquitto service is running
systemctl status mosquitto.service

# Check if the MQTT port 1883 is listening
ss -ltn | grep 1883

# Edit the distrobox Mosquitto service file
sudo nano /etc/systemd/system/mosquitto-distrobox.service

# Reload the systemd daemon configuration
sudo systemctl daemon-reload

# Enable the distrobox Mosquitto service to start on boot
sudo systemctl enable mosquitto-distrobox.service

# Start the distrobox Mosquitto service
sudo systemctl start mosquitto-distrobox.service

# Check if the Mosquitto service is running
systemctl status mosquitto.service

# Install the paho-mqtt Python library for MQTT communication
pip install paho-mqtt

'''



# Install: pip install paho-mqtt
import paho.mqtt.client as mqtt
import time

# MQTT settings
BROKER = "steamini.local"
PORT = 1883
TOPIC = "hello/mqtt"

# Callback when connected to broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

# Create client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
try:
    client.connect(BROKER, PORT, keepalive=60)
except ConnectionRefusedError:
    print(f"Cannot connect to broker at {BROKER}:{PORT}")
    exit(1)

# Start the network loop
client.loop_start()

# Publish messages
try:
    for i in range(5):
        message = f"Hello MQTT {i}"
        client.publish(TOPIC, message)
        print(f"Published: {message}")
        time.sleep(1)
    
    # Keep the script running to receive messages
    time.sleep(5)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    client.loop_stop()
    client.disconnect()
