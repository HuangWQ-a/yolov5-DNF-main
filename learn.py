

import numpy as np
from PIL import Image

# 加载.npy文件为NumPy数组
array = np.load(r'D:\work\DNF\yolov5-DNF-main\问号模板.npy')

# 将NumPy数组转换为PIL图像对象
image = Image.fromarray(array)

# 保存图像文件
image.save('image.jpg')