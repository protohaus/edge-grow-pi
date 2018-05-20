from flask import Flask

from avahi.service import AvahiService

## Web server
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World in collaboration with Avahi and DBUS!'

if __name__ == "__main__":
    mqttAvahi = AvahiService("Mosquitto MQTT Broker", "_mqtt._tcp", 1883)
    app.run(host='0.0.0.0', port=80)
