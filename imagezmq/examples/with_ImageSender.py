"""with_ImageSender.py -- demonstrate using ImageSender class in with statement.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream. Images are jpg compressed before sending.

This program requires that the image receiving program be running first. Brief
test instructions are in that program: with_ImageHub.py.

"""

import sys
import socket
import time
import traceback
import cv2
from imutils.video import VideoStream
import imagezmq

# use either of these formats to specifiy address of display computer
#     with imagezmq.ImageSender(connect_to='tcp://jeff-macbook:5555')
#     with imagezmq.ImageSender(connect_to='tcp://192.168.1.190:5555')
# change the line below: with imagezmq.ImageSender()... as needed

rpi_name = socket.gethostname()  # send RPi hostname with each image
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up
jpeg_quality = 95  # 0 to 100, higher is better quality, 95 is cv2 default
try:
    with imagezmq.ImageSender(connect_to='tcp://192.168.86.34:5555') as sender:
        while True:  # send images as stream until Ctrl-C
            image = picam.read()
            ret_code, jpg_buffer = cv2.imencode(
                ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            reply_from_mac = sender.send_jpg(rpi_name, jpg_buffer)
            # above line shows how to capture REP reply text from Mac
except (KeyboardInterrupt, SystemExit):
    pass  # Ctrl-C was pressed to end program
except Exception as ex:
    print('Python error with no Exception handler:')
    print('Traceback error:', ex)
    traceback.print_exc()
finally:
    picam.stop()  # stop the camera thread
    sys.exit()
