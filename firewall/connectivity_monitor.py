import NetworkManager, time, os, raven

# Host to ping to check connectivity
hostname = "google.com"

client = raven.Client(os.environ.get('SENTRY_DSN'))

if __name__ == "__main__":
    # Give the system 5 minutes to start up
    print("Waiting 5 minutes before monitoring connection")
    time.sleep(5*60)
    
    while(True):
        response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
        
        if response == 0:
          print(hostname + ' is up!')
        else:
          print(hostname + ' is down!')
          NetworkManager.NetworkManager.WirelessEnabled = False
          time.sleep(5)
          NetworkManager.NetworkManager.WirelessEnabled = True
          time.sleep(50)
          client.captureMessage('Network was down. WiFi connections have been restarted.')
        
        time.sleep(10)
