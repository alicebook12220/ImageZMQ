import socket
from socket import error as SocketError
import cv2

import sys
import numpy as np
import time
address = ('192.168.23.22', 5005)  # 伺服器端地址和埠
ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser.bind(address)
ser.listen(5)
# 阻塞式
print('waiting。。。')
conn, addr = ser.accept()
print('建立連線...')
print('連線物件：', addr)
# cap = cv2.VideoCapture(r"D:projectdatasetvideo測試.mp4")
cap = cv2.VideoCapture(0)
frames_num=cap.get(7)
print('視訊總幀數：',frames_num)
print('傳送目標...')
count = 0
while cap.isOpened():
    try:
        time.sleep(0.1)
        data = conn.recv(1024)
        data = data.decode()
        if not data:
            break
        ret, frame = cap.read()
        #frame = cv2.resize(frame,(1280,720))
        cv2.imshow('send', frame)
        cv2.waitKey(1)
        count += 1
        # 資料打包有很多方式，也可以用json打包
        img_encode = cv2.imencode('.jpg', frame)[1]

        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()

        conn.sendall(str_encode)
    except SocketError as e:
        print('KeyboardInterrupt')
        #sys.exit(0)