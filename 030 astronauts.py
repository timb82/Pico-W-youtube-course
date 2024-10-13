import network
import time
import urequests
from secret import SSID, PASSWD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWD)

while not wlan.isconnected():
    print("...connecting...", end="\r", flush=True)
    time.sleep(1)

server_IP = wlan.ifconfig()[0]
print("connected as", server_IP)
astronauts = urequests.get("http://api.open-notify.org/astros.json").json()

for a in astronauts["people"]:
    print(a["name"])
