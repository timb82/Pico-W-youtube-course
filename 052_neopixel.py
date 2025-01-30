import neopixel
from machine import Pin
from time import sleep

PIX_PIN = 0
PIX_SIZE = 8
pix = neopixel.NeoPixel(Pin(PIX_PIN, Pin.OUT), PIX_SIZE)

palette={"red" : [255,0,0],
"orange" : [255,60,0],
"green" : [0, 255, 0],
"turquoise" : [0,255,125],
"cyan" : [0,255,255],
"mint" : [0,255,80],
"ocean" : [0,50,255],
"blue" : [0, 0, 255],
"violet" : [125,0,255],
"pink" : [255,0,100],
"raspberry" : [255,0,150],
"white" : [255,255,255],
"off" : [0,0,0],
"exit" : [0,0,0],
}
# pix[0] = off
# pix.fill[(0, 0, 255))
# pix.write()


print(f"Color list:")
for key in palette.keys():
    print(key, end=", ")

print("")
while True:
    try:
        color = input(f"\nEnter color: ")
        if color == "exit": raise KeyboardInterrupt

        for i in range(PIX_SIZE):
            # pix[i]=(25*(i+1),0,10*(i+1))
            pix[i]=palette[color]
        pix.write()
   
    except KeyboardInterrupt:
        for i in range(PIX_SIZE):
            pix[i]=palette['off']
        pix.write()
        break
    
    except KeyError:
        print("Color not defined!")