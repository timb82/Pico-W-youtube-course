import network
import time
from secrets2 import SSID, PASSWD

# This script automatically connects to Wi-Fi on startup.
# No browser or user interaction is required.


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWD)

    print("Connecting to Wi-Fi...")
    max_retries = 5
    retries = 0
    while not wlan.isconnected() and retries < max_retries:
        retries += 1
        print(f"Attempt {retries}...", end="\t")
        time.sleep(2)
        print("Status: ", wlan.status())

    if wlan.isconnected():
        print("Connected to Wi-Fi!")
        print("IP Address:", wlan.ifconfig()[0])
    else:
        print("Failed to connect to Wi-Fi.")
        wlan.active(False)


# Main execution: automatically connect on startup
connect_to_wifi()
