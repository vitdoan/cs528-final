from socket import *

droneIP = "192.168.10.1"
dronePort = 8889

sock = socket(AF_INET, SOCK_DGRAM)

inp = ""

while inp != "Q":
    inp = input("Enter command")
    sock.sendto(inp.encode(), (droneIP, dronePort))
    modifiedMessage, serverAddress = sock.recvfrom(2048)
    print(modifiedMessage.decode())
sock.close()
