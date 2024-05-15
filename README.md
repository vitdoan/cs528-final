# Controlling drone with hand gestures using MPU6050 and ESP32-S3

This project aims to control a Tello drone utilizing only hand gestures (up, down, left and right) while holding an MPU6050. The MPU6050 outputs accelerometer and gyroscope data which get fed into a machine learning algorithm that outputs its classification. We use this classification as well as the acceleration data to send a command to the Tello drone in order for it to move.



## How to use example

Download the code and build it. Upload it to your ESP32 that has a MPU6050 attached to it with SDA pin at 0 and SLA pin at 1 (You can change these in the main.c code). In addition add 3 buttons, one button on pin 4 that will activate the up, down, left and right actions, one button on pin 5 that will activate the forward, backward, counter clockwise and clockwise actions, and one on pin 6 that will land the drone. Keep the ESP32 attached to your computer and change the autocollection.py port to match your device. Then connect to your Tello's wifi and run the autocollection.py and use up, down, left and right as seen in the video to do commands. Press the button to activate the collection and it will collect for 3 seconds and after classification will send the signal to the drone. 

## Sample video

https://www.youtube.com/watch?v=AQQGD5aCq7M
