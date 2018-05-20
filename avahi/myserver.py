from avahi.service import AvahiService

if __name__ == "__main__":
    mqttAvahi = AvahiService("Mosquitto MQTT Broker", "_mqtt._tcp", 1883)
