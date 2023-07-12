# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:14:29 2020

@author: analoganddigital   ( GitHub )



这段代码是一个用于截取屏幕截图的函数。它使用了win32gui、win32api、win32con和win32ui等Python库来操作Windows系统的图形界面。

函数的参数是一个可选的截图区域（region），通过传入左上角和右下角的坐标来指定特定区域的截图。如果没有传入region参数，则默认截取整个屏幕。

函数内部首先获取桌面窗口的句柄（hwin），然后根据传入的region参数或系统的虚拟屏幕参数来计算截图区域的宽度、高度、左上角和顶部坐标。

接下来，函数获取桌面窗口的设备上下文句柄（hwindc），并使用CreateDCFromHandle函数创建与之相关联的设备上下文（srcdc）。然后使用CreateCompatibleDC创建一个与设备上下文兼容的内存设备上下文（memdc）。

接下来，函数使用CreateCompatibleBitmap创建一个与设备上下文兼容的位图（bmp），并将其选入内存设备上下文（memdc）。然后使用BitBlt函数将桌面窗口上指定区域的图像复制到位图上。

然后，函数使用GetBitmapBits将位图的像素数据获取为一个有符号整数数组（signedIntsArray），再使用np.fromstring将其转换为无符号整数数组（img）。最后，函数清理创建的设备上下文对象，释放窗口设备上下文，并删除位图对象。

最后，函数返回截取的屏幕图像（img）。

总的来说，这段代码实现了一个简单的屏幕截图功能。

"""
import numpy as np
import win32api
import win32con
import win32gui
import win32ui


def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img
