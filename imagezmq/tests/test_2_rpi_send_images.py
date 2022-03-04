"""test_2_rpi_send_images.py -- send PiCamera image stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream.

This program requires that the image receiving program be running first. Brief
test instructions are in that program: test_2_mac_receive_images.py.
"""

import sys

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq

cap_0 = cv2.VideoCapture(0)
cap_1 = cv2.VideoCapture(1)
# use either of the formats below to specifiy address of display computer
# sender = imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.23.22:5555')

rpi_name = socket.gethostname()  # send RPi hostname with each image
#picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    #image = picam.read()
    ret_0, frame_0 = cap_0.read()
    ret_1, frame_1 = cap_1.read()
    frame_h_0 = cv2.hconcat([frame_0, frame_1])
    frame_h_1 = cv2.hconcat([frame_0, frame_1])
    frame = cv2.vconcat([frame_h_0, frame_h_1])
    #print(frame.shape)
    sender.send_image(rpi_name, frame)
    #cv2.imshow('frame', frame)
    #key = cv2.waitKey(1)