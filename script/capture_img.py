# 读取视频文件，随机提取几张截图
import cv2
import numpy as np
  
def save_image(image, dir, num):
    path = dir + str(num) + '.jpg'
	cv2.imwrite(path, image)
  
videoCapture = cv2.VideoCapture("123.mp4")

#读帧
success, frame = videoCapture.read()
i = 0
timeF = 290 #播放速度（即取截图频率），假如一秒有29帧，相当于快进10倍播放
j = 0
while success :
i = i + 1
	if (i % timeF == 0):
		j = j + 1
		save_image(frame,"D:/QQ/10018637/Video/image/",j)
		print('save image:', j)
	success, frame = videoCapture.read()
