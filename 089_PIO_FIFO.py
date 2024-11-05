from machine import Pin
from time import sleep
import rp2

LS_PIN=16
dt = 0.3

@rp2.asm_pio(out_init=(rp2.PIO.IN_LOW,)*4)
def pio_prog():
    wrap_target()
    pull()
    mov(x, osr)
    mov(y, x)
    mov(isr, y)
    mov(pins,y)
    push()
    wrap ()

sm0 = rp2.StateMachine(0, pio_prog, freq=2000, out_base=Pin(LS_PIN))

sleep(.1)
print(20*'=')
print('Python program start')
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print('Put a 0xA')
sm0.put(0xA)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print("SM running")
sm0.active(True)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print("SM stopped")
sm0.active(0)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print('Put a 0xB')
sm0.put(0xB)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")


print('Put a 0xC')
sm0.put(0xC)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print('Put a 0xD')
sm0.put(0xD)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print('Put a 0xE')
sm0.put(0xE)
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")

# print('Put a 0xF')
# sm0.put(0xF)
# sleep(dt)
# tx_cnt = sm0.tx_fifo()
# rx_cnt = sm0.rx_fifo()
# print(f"tx={tx_cnt}\trx={rx_cnt}\n")

print("Get from Rx")
out = sm0.get()
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\treceived data:{hex(out)}\n")

print("SM running")
sm0.active(True)
sleep(dt)
sm0.active(False)
print("SM stopped")
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\n")


print("Get from Rx")
out = sm0.get()
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\treceived data:{hex(out)}\n")

print("Get from Rx")
out = sm0.get()
sleep(dt)
tx_cnt = sm0.tx_fifo()
rx_cnt = sm0.rx_fifo()
print(f"tx={tx_cnt}\trx={rx_cnt}\treceived data:{hex(out)}\n")