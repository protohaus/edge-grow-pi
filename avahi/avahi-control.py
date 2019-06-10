import time

from avahi.service import AvahiService

if __name__ == "__main__":
    # Publish address and port of MQTT server running in mosquitto service
    mqttAvahi = AvahiService("Mosquitto MQTT Broker", "_mqtt._tcp", 1883)

    # Sleep forever to keep mDNS service broadcast alive
    while True:
        time.sleep(60)

