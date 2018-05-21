echo "Blocking port 1883 on all interfaces except $MOSQUITTO_INTERFACE"
iptables -A INPUT -i !$MOSQUITTO_INTERFACE -p tcp --destination-port 1883 -j DROP
/usr/sbin/mosquitto -c /mqtt/config/mosquitto.conf
