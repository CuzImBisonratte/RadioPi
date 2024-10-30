import time
import socket
from machine import Pin
from ir_tx.nec import NEC

addr = 0x0401
data = {
    "power": 0x04,	"eject": 0x08,	"menu": 0x47,
    "10dwn": 0x4B,	"volUp": 0x4C,	"10up": 0x4D,
    "back": 0x4E,	"pause": 0x4F,	"frwd": 0x50,
    "foldDwn": 0x51,"volDwn": 0x52,	"foldUp": 0x53,
    "sleep": 0x54,	"intro": 0x55,	"info": 0x56,
    "src": 0x57,	"eq": 0x59,		"stop": 0x5A,
    "prog": 0x5B,	"clock": 0x5D,	"mute": 0x5E
}


nec = NEC(Pin(17, Pin.OUT, value = 0))
nec.transmit(addr, data["mute"])
