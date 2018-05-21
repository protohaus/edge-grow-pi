echo "Blocking port 1883 on internet connected $INTERNET_INTERFACE"
#iptables -A INPUT -i $INTERNET_INTERFACE -p tcp --destination-port 1883 -j DROP
/usr/sbin/mosquitto -c /mqtt/config/mosquitto.conf
