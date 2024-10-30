# Settings
ADDR = 0x0401
DATA = {
    "power": 0x04,	"eject": 0x08,	"menu": 0x47,
    "10dwn": 0x4B,	"volUp": 0x4C,	"10up": 0x4D,
    "back": 0x4E,	"pause": 0x4F,	"frwd": 0x50,
    "foldDwn": 0x51,"volDwn": 0x52,	"foldUp": 0x53,
    "sleep": 0x54,	"intro": 0x55,	"info": 0x56,
    "src": 0x57,	"eq": 0x59,		"stop": 0x5A,
    "prog": 0x5B,	"clock": 0x5D,	"mute": 0x5E
}
WIFI_SSID=""
WIFI_PASS=""

# Libraries
import time
import socket
import network
from machine import Pin
from ir_tx.nec import NEC

# Network Stuff
network.country('DE')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140) # Disable WiFi Standby
wlan.connect(WIFI_SSID, WIFI_PASS)

# Webserver (API)
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(1)

# Connect to wifi
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
    
# Setup IR Blaster
nec = NEC(Pin(17, Pin.OUT, value = 0))
    
# Webserver
while True:
    try:
        # Accept traffic
        conn, addr = server.accept()
        print('HTTP-Request von Client', addr)
        request = conn.recv(1024)
        # Handle request
        request = str(request)
        request = request.split()
        if "/cmd/" in request[1]:
            cmd = request[1].replace("/cmd/", "")
            print(cmd)
            if cmd in DATA:
                conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
                conn.send('{"success":true,"cmd":"'+cmd+'"}')
                # Send IR Command
                nec.transmit(ADDR, DATA[cmd])
            else:
                conn.send('HTTP/1.0 404 NOT FOUND\r\nContent-type: application/json\r\n\r\n')
                conn.send('{"cmd":"Not found"}')
        # Custom command for max vol
        elif request[1] == "/volMax":
            for i in range(32):
                nec.transmit(ADDR, DATA["volUp"])
                time.sleep(0.3)
            conn.send('HTTP/1.0 200 OK\r\n\r\n')
        # Custom command for startup sequence
        elif request[1] == "/init":
            conn.send('HTTP/1.0 200 OK\r\n\r\n')
            nec.transmit(ADDR, DATA["power"])
            time.sleep(7.5)
            for i in range(4):
                nec.transmit(ADDR, DATA["src"])
                time.sleep(1)
            time.sleep(5)
            for i in range(32):
                nec.transmit(ADDR, DATA["volUp"])
                time.sleep(0.3)
        else:
            conn.send('HTTP/1.0 404 NOT FOUND\r\nContent-type: application/json\r\n\r\n')
            conn.send('{"cmd":"Not found"}')
        conn.close()
    except OSError as e:
        break
    except (KeyboardInterrupt):
        break