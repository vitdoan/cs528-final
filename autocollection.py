import serial
import os
import time
import numpy as np
import threading
from socket import *
from predictHandGesture import predictHandGesture

serial_name = "/dev/cu.usbserial-1410"
script_dir = os.path.dirname(__file__)
ser = serial.Serial(serial_name, 115200)

droneIP = "192.168.10.1"
dronePort = 8889
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(2)
# sock.bind((gethostname(), 8889))

time_window = 3
sampling_rate = 100

lock = threading.Lock()
classification = ""
movement = 0


# Get acceleration for scaling
def get_acceleration(count):
    global movement
    file = open(
        "./collected.txt",
        "r",
    )
    maxAccel = 0
    for i in range(count):
        line = file.readline()
        firstComma = line.index(",")
        secondComma = line.index(",", firstComma + 1)
        thirdComma = line.index(",", secondComma + 1)
        x = int(line[0:firstComma])
        y = int(line[firstComma + 2 : secondComma])
        z = int(line[secondComma + 2 : thirdComma])
        maxAccel = max(maxAccel, (x**2 + y**2 + z**2) ** 0.5)
    file.close()
    # Minimum speed is 25000 and maximum is 40000
    acceleration = min(max(maxAccel - 25000, 0), 15000)
    move = int(30 + acceleration / 500)
    lock.acquire()
    movement = move
    lock.release()


# Get classification from model
def get_classification():
    global classification
    classif = predictHandGesture("./collected.txt")
    lock.acquire()
    classification = classif
    lock.release()


# Start command©
# while True:
try:
    sock.sendto(("command").encode(), (droneIP, dronePort))
    # modifiedMessage, serverAddress = sock.recvfrom(2048)
    # if modifiedMessage.decode() == "ok":
    #     break
    # print(modifiedMessage.decode())
except Exception as e:
    print(e)

# # Set speed
# # while True:
try:
    sock.sendto(("speed 2").encode(), (droneIP, dronePort))
    # modifiedMessage, serverAddress = sock.recvfrom(2048)
    # if modifiedMessage.decode() == "ok":
    #     break
    # print(modifiedMessage.decode())
except Exception as e:
    print(e)

# Start takeoff
# while True:
try:
    sock.sendto(("takeoff").encode(), (droneIP, dronePort))
    # modifiedMessage, serverAddress = sock.recvfrom(2048)
    # if modifiedMessage.decode() == "ok":
    #     break
    # print(modifiedMessage.decode())
except Exception as e:
    print(e)

print("Collecting")
while True:
    # Wait for start signal
    waiting = ""
    while waiting != "Normal" and waiting != "Changed" and waiting != "Land":
        waiting = ser.readline().decode().strip()
        print(waiting)

    if waiting == "Land":
        # while True:
        try:
            sock.sendto(("land").encode(), (droneIP, dronePort))
            modifiedMessage, serverAddress = sock.recvfrom(2048)
            # if modifiedMessage.decode() == "ok":
            #     break
            print(modifiedMessage.decode())
        except Exception as e:
            print(e)
        break

    data = np.array([])
    start_time = time.time()
    count = 0
    try:
        while time.time() - start_time < time_window:
            collected = ser.readline()
            collected = collected.decode().strip()
            if collected.count(",") != 5:
                continue
            data = np.append(data, collected)
            count += 1
            time_diff = start_time + (1 / sampling_rate * count)
            wait_time = time_diff - time.time()
            time.sleep(max(0, wait_time))
        print("Samples collected: " + str(np.shape(data)))
        file = open(
            "./collected.txt",
            "w",
        )
        for i in data:
            file.write(i + "\n")
    except Exception as e:
        print(e)
        break
    file.close()
    thread1 = threading.Thread(target=get_acceleration, args=((count,)))
    thread2 = threading.Thread(target=get_classification, args=())
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    modifiedMessage = ""
    message = ""
    # while modifiedMessage != "ok":\
    if waiting == "Normal":
        print("Normal")
        print(movement)
        print(classification)
    elif waiting == "Changed":
        print("Changed")
        print(movement)
        print(classification)
    else:
        print("Broken :(")
        print(movement)
        print(classification)
    try:
        if waiting == "Normal":
            if classification == "Right":
                message = "right " + str(movement)
            elif classification == "Left":
                message = "left " + str(movement)
            elif classification == "Up":
                message = "up " + str(movement)
            elif classification == "Down":
                message = "down " + str(movement)
        elif waiting == "Changed":
            if classification == "Right":
                rotation = (movement - 20) * 4 + 30
                message = "cw " + str(rotation)
            elif classification == "Left":
                rotation = (movement - 20) * 4 + 30
                message = "ccw " + str(movement)
            elif classification == "Up":
                message = "forward " + str(movement)
            elif classification == "Down":
                message = "back " + str(movement)
        else:
            print("Broken :(")
            modifiedMessage = "ok"
            message = "land"
        sock.sendto((message).encode(), (droneIP, dronePort))
        # modifiedMessage, serverAddress = sock.recvfrom(2048)
        # print(modifiedMessage.decode())
    except Exception as e:
        print(e)
    print("Done cycle")
