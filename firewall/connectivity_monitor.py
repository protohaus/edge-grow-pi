import NetworkManager, time, os, raven, dbus

# Host to ping to check connectivity
hostname = "google.com"

client = raven.Client(os.environ.get('SENTRY_DSN'))

def activate_wifi_connection(name):
    connections = NetworkManager.Settings.ListConnections()
    connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
    conn = connections[name]
    
    ctype = conn.GetSettings()['connection']['type']
    
    # Check if the specified connection is a WiFi connection
    if ctype == '802-11-wireless':
        devices = NetworkManager.NetworkManager.GetDevices()
        
        # Go through all available WiFi devices and find unactivated ones
        for dev in devices:
            if(dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and
                    dev.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED):
                # Try three times (Enable WiFi and then assign connection to device)
                for i in range(3):
                    try:
                        NetworkManager.NetworkManager.WirelessEnabled = True
                        time.sleep(5)
                        NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
                        break
                    except dbus.exceptions.DBusException:
                        client.captureMessage('Failed to connect to WiFi. Try {}'.format(i))
            
                # Check if really connected
                time.sleep(30)
                if(dev.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED):
                    client.captureMessage('Failed to connect to {}'.format(name))
    else:
        client.captureMessage('Connection ({}) not a WiFi network ({})'.format(name, ctype))

if __name__ == "__main__":
    # Give the system 5 minutes to start up
    print("Waiting 10 minutes before monitoring connection")
    time.sleep(600)

    print("Starting connectivity monitoring")
    while(True):
        response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
        
        if response != 0:
            print(hostname + ' is down!')
            
            NetworkManager.NetworkManager.WirelessEnabled = False
            time.sleep(5)
            activate_wifi_connection('balena-wifi-01')
            NetworkManager.NetworkManager.WirelessEnabled = True
            time.sleep(60)
            client.captureMessage('Network was down. WiFi connections have been restarted.')
        
        time.sleep(10)
