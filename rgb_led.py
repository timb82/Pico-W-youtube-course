from machine import Pin, PWM
from utime import sleep

RPIN = 13
GPIN = 11
BPIN = 10

r_led = PWM(Pin(RPIN))
g_led = PWM(Pin(GPIN))
b_led = PWM(Pin(BPIN))

led = [r_led, g_led, b_led]

for l in led:
    l.freq(1000)
    l.duty_u16(0)

def color(R,G,B):
    for color in zip(led, [R,G,B]):
        color[0].duty_u16(color[1])

mx = 65550
while True:
    try:
        my_color = input('What color do you want? ')
        try: 
            my_color = int(my_color)
        except ValueError:
            pass

        try:
            if my_color.count(',') ==2:
                my_color = (my_color.split(','))
                my_color = tuple(int(x) for x in my_color)
        except ValueError:
            pass

        if type(my_color) is tuple and len(my_color)==3:
            color(*my_color)
        elif my_color is "red" or my_color is 1:
            color(mx,0,0)
        elif my_color is 'green' or my_color is 2:
            color(0,mx,0)
        elif my_color is 'blue' or my_color is 3:
            color(0,0,mx)
        elif my_color is 'cyan' or my_color is 4:
            color(0,mx,mx)
        elif my_color is 'magenta' or my_color is 5:
            color(mx,0,mx)
        elif my_color is 'yellow' or my_color is 6:
            color(mx,50000,0)
        elif my_color is 'orange' or my_color is 7:
            color(mx,0,10000)
        elif my_color is 'white' or my_color is 8:
            color(mx,mx,mx)
        else:
            print(f"unknown color: {my_color}")
            color(0,0,0)
    except KeyboardInterrupt:
        print('bye')
        for l in led:
            l.duty_ns(0)
        break