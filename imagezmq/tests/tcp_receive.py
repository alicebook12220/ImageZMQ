import socket
import sys
import cv2
import numpy as np
import time
address = ('192.168.23.22', 5005)  # 伺服器端地址和埠
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cli.connect(address)  # 嘗試連線伺服器端
except Exception:
    print('[!] Server not found or not open')
    sys.exit()

frame_count = 1
while True:
    print(frame_count)
    #time1 = time.time() if frame_count == 1 else time1
    trigger = 'ok'
    cli.sendall(trigger.encode())
    data = cli.recv(1024*1024*20)
    image = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    print(frame_count)
    print(image.shape)
    #cv2.imshow('video',image)
    cv2.waitKey(10)
    #end_time = time.time()
    #time2 = time.time()
    #print(image.shape[:2], int(frame_count / (time2 - time1)))
    frame_count += 1
cli.close()