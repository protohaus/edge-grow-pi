Add the folllowing line to `resin-boot/config.txt`

    dtoverlay=pi3-disable-wifi

Add the files in `system-connections` to the folder in `resin-boot/system-conncetions`

Ensure that the *id* in the WiFi system connection (`system-connections/resin-wifi-01`) equals the *name* used in the connectivity monitor (`firewall/connectivity_monitor.py`).