from machine import Pin, I2C, PWM
from utime import sleep
from array import array
from ssd1306 import SSD1306_I2C
from rotary import RotaryIRQ
from machine import Pin

CLK_PIN = 28
DT_PIN = 27
SW_PIN = 26
STEP = 5
RPIN = 13
GPIN = 11
BPIN = 10



def cursor(chn):
    x = 5
    y = 11 + chn*18
    coords = array("i", [0,0, 0,6, 3,3, 0,0])
    display.rect(x,10,4,47,0,True)
    display.poly(x,y, coords,1, True)
    display.show()

def bar(rgb, chn):
    x = 30 # X-coord of a bar
    y = 10 # Y- coord of a bar
    w = 60 # bar width
    h = 10 # bar height
    dy = 18 # offset between lines
    dx = 16 # offset for label before a bar
    chn_list = ['R', 'G', 'B'] # labels
    display.text(chn_list[chn], x-dx, y+dy*chn+1)
    display.rect(97, y+dy*chn,31,8,0,True)
    display.text(str(int(rgb[chn]))+"%",97,y+dy*chn)
    display.rect(x, y + dy * chn, w, h, 1, False)
    display.rect(x+2, y+2 + dy*chn, w-2, h-2, 0, True)
    display.rect(x+2, y+2 +dy*chn, int(rgb[chn]*(w-4)/100), h-4, 1, True)
    display.show()


# Setup hardware
i2c = I2C(id=1, sda=Pin(6), scl=Pin(7))
display = SSD1306_I2C(128, 64, i2c)

r = RotaryIRQ(pin_num_clk=28,
              pin_num_dt=27,
              min_val=0,
              max_val=int(100/STEP),
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

btn = Pin(26, Pin.IN, Pin.PULL_UP)

led = [PWM(Pin(RPIN)), PWM(Pin(GPIN)), PWM(Pin(BPIN))]

val_old = r.value()
btn_old = 1

chn = 0
rgb = [25/STEP,25/STEP,25/STEP]
chn_list = ['R', 'G', 'B']

cursor(chn)

for l, val in zip(led, rgb):
    l.freq(1000)
    l.duty_u16(int(val/100*(2**16-1)))


r.set(value=rgb[chn])
for c in range(len(rgb)):
    bar(rgb,c)

# r.value(rgb[chn])
while True:
    try:
        val_new = r.value()
        btn_new = btn.value()

        if val_old != val_new:
            val_old = val_new
            print(f'{chn_list[chn]}={val_new*STEP}')
            rgb[chn] = val_new*STEP
            led[chn].duty_u16(int(val_new*STEP/100*(2**16-1)))
            bar(rgb,chn)

        if btn_new is 0 and btn_old is 1:
            if chn<2:
                chn +=1
            else:
                chn =0
            cursor(chn)
            r.set(value=rgb[chn]/STEP)

        
        btn_old = btn_new
        sleep(0.05)
    except KeyboardInterrupt:
        display.fill(0)
        display.poweroff()
        for l in led:
            l.duty_u16(0)
        break
