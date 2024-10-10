from rotary import RotaryIRQ
from machine import Pin
from utime import sleep_ms


r = RotaryIRQ(pin_num_clk=28,
              pin_num_dt=27,
              min_val=0,
              max_val=50,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

sw = Pin(26, Pin.IN, Pin.PULL_UP)
val_old = r.value()
sw_old = 1
while True:
    val_new = r.value()
    sw_new = sw.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    if sw_new is 0 and sw_old is 1:
        print("click!")
    
    sw_old = sw_new
    sleep_ms(50)