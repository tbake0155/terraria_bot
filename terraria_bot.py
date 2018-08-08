import argparse
import cv2
import numpy as np
import os
import threading
import win32api
import mouseEvent
import keyEvent
import pyautogui
from time import sleep

screen_width, screen_height = pyautogui.size()

search_width_left = screen_width - (3 * (screen_width / 4))
search_height_top = screen_height - (2 * (screen_height / 3))

print_lock = threading.Lock()

def thread_safe_print(*args):
    with print_lock:
        for arg in args:
            print arg

screenshot_lock = threading.Lock()

screenshot = pyautogui.screenshot

def Screenshot():
    with screenshot_lock:
        global screenshot
        return screenshot

def Screenshot(new_screenshot):
    with screenshot_lock:
        global screenshot
        screenshot = new_screenshot

explorer = False
trigger = False
quitter = False
allThreadsDie = False

explorer_keys = [0x06] # X2 mouse click
trigger_keys = [0x05] # X1 mouse click
quitter_keys = [0x23] # End

explorer_lock = threading.Lock()
trigger_lock = threading.Lock()
quitter_lock = threading.Lock()


def Explorer():
    global explorer
    with explorer_lock:
        return explorer

def Explorer(explorerValue):
    global explorer    
    with quitter_lock:
        quitter = quitterValue

def ExplorerToggle():
    global explorer
    with explorer_lock:
        explorer = not explorer
        
def Trigger():
    global trigger
    with trigger_lock:
        return trigger

def Trigger(triggerValue):
    global trigger
    with trigger_lock:
        trigger = triggerValue

def TriggerToggle():
    global trigger
    with trigger_lock:
        trigger = not trigger

def Quitter():
    global quitter
    with quitter_lock:
        return quitter

def Quitter(quitterValue):
    global quitter    
    with quitter_lock:
        quitter = quitterValue

def QuitterToggle():
    global quitter
    with quitter_lock:
        quitter = not quitter

class ExplorerWatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event() 

    def run(self):
        while True:
            for i in range(1, 256):
                if win32api.GetAsyncKeyState(i):
                    if i in explorer_keys:
                        ExplorerToggle()
                        sleep(0.5)
                    else:
                        pass
            sleep(0.01)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class TriggerWatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event() 

    def run(self):
        while True:
            for i in range(1, 256):
                if win32api.GetAsyncKeyState(i):
                    if i in trigger_keys:
                        TriggerToggle()
                        sleep(0.5)
                    else:
                        pass
            sleep(0.01)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class ExitWatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event() 

    def run(self):
        while True:
            for i in range(1, 256):
                if win32api.GetAsyncKeyState(i):
                    if i in quitter_keys:
                        QuitterToggle()
                        sleep(0.5)
                    else:
                        pass
            sleep(0.01)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class EagleEye(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event() 

    def run(self):
        while True:
            new_screenshot = pyautogui.screenshot()
            Screenshot(new_screenshot)
            sleep(0.03)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def main():
    #explorerWatcher = ExplorerWatcher()
    triggerWatcher = TriggerWatcher()
    exitWatcher = ExitWatcher()
    #eagleEye = EagleEye()

    #explorerWatcher.start()
    triggerWatcher.start()
    exitWatcher.start()
    #eagleEye.start()
    
    while not quitter:
        if trigger:
            mouseEvent.leftClick()
        #if explorer:
        #    keyEvent.pressAndHold('a','s')
        sleep(0.01)

    #explorerWatcher.stop()
    triggerWatcher.stop()
    exitWatcher.stop()
    #eagleEye.stop()

main()
