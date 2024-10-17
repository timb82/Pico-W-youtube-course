import network
import time
import urequests
from secret import SSID, PASSWD, OWM_API_KEY

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWD)

while not wlan.isconnected():
    print("...connecting...", end="\r", flush=True)
    time.sleep(1)

server_IP = wlan.ifconfig()[0]
print("connected as", server_IP)
weather = urequests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q=Krakow,Poland&appid={OWM_API_KEY}&units=metric"
).json()


def tup2time(tup, incl_date=False):
    if incl_date:
        return f"{tup[3]}:{tup[4]}\t{tup[2]}/{tup[1]}/{tup[0]}"
    else:
        return f"{tup[3]}:{tup[4]}"


# print(weather)
tm = time.localtime(weather["dt"] + weather["timezone"])
sr = time.localtime(weather["sys"]["sunrise"] + weather["timezone"])
ss = time.localtime(weather["sys"]["sunset"] + weather["timezone"])
print(f"Welcome to {weather['name']}, {weather['sys']['country']}")
print(f"Local time: {tup2time(tm)}")
print(f"Sunrise at: {tup2time(sr)} AM")
print(f"Sunset at:  {tup2time(ss)} PM")

print(
    f"Current temp: {weather['main']['temp']}\nMax temp: {weather['main']['temp_max']}\nMin temp: {weather['main']['temp_min']}"
)
print(f"Humidity: {weather['main']['humidity']}%")
print(f"Barometric pressure {weather['main']['pressure']} hPa")
print(f"Current conditions: {weather['weather'][0]['main']}")
print(f"Wind: {weather['wind']['speed']} kph")
