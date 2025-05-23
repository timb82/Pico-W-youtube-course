import time
import network
from secrets import SSID, PASSWD


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWD)

max_wait = 100
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        print(str(wlan.status()))
        break
    max_wait -= 1
    print("waiting for connection")
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError("network connection failed")
else:
    print("connected")
    status = wlan.ifconfig()
    print("ip = " + status[0])
