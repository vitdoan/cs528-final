import serial
import os
import time
import numpy as np

serial_name = "/dev/cu.usbserial-14230"
script_dir = os.path.dirname(__file__)
ser = serial.Serial(serial_name, 115200)

time_window = 2
sampling_rate = 100

file_count = 0
file_name_addendum = ""
data_collected = "Up"

while True:
    inp = input("Press enter to start collecting (q to quit, r to redo previous)")
    if inp == "q":
        break
    elif inp == "r":
        file_count -= 1
    data = np.array([])
    start_time = time.time()
    count = 0
    try:
        while ser.in_waiting:
            ser.readline()
        while count < time_window * sampling_rate:
            data = np.append(data, ser.readline())
            count += 1
        print("Samples collected: " + str(np.shape(data)))
        file = open(
            "./"
            + data_collected
            + "/"
            + file_name_addendum
            + str(file_count).zfill(2)
            + ".txt",
            "w",
        )
        for i in data:
            string = i.decode().strip()
            comma_count = 0
            for j in string:
                if j == ",":
                    comma_count += 1
            if comma_count != 5:
                print("Missed a datapoint")
                raise (Exception)

        for i in data:
            file.write(i.decode().strip() + "\n")
        file_count += 1
    except:
        print("Error occured, try again")
        if inp == "r":
            file_count += 1
    file.close()
