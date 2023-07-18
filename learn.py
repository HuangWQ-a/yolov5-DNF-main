import cv2

# 读取图像
image = cv2.imread(r"D:\work\DNF\yolov5-DNF-main\test\DNF.jpg")

# 检查图像的通道数
channels = image.shape[2]

print("图像的通道数：", channels)