import win32api
import win32con
import time

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)

