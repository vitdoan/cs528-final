import serial
import os
import time
import numpy as np
import threading
from socket import *

droneIP = "192.168.10.1"
dronePort = 8889
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(3)

while True:
    sock.sendto(("land").encode(), (droneIP, dronePort))
    modifiedMessage, serverAddress = sock.recvfrom(2048)
    print(modifiedMessage.decode())
    if modifiedMessage.decode() == "ok":
        break
    print(modifiedMessage.decode())
