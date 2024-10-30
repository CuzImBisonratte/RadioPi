import time
from machine import Pin
from ir_rx.nec import NEC_8  # NEC remote, 8 bit addresses

def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        print('Repeat code.')
    else:
        print('Data {:02x} Addr {:04x}'.format(data, addr))

ir = NEC_8(Pin(16, Pin.IN), callback)
while True:
    time.sleep_ms(500)