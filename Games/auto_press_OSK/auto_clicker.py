import pyautogui
import time
import os
import sys
import threading

from pynput.keyboard import Listener, Key

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
start_stop_key = Key.f3
exit_key = Key.f4

# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'Clicked at X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.running = False
        self.program_running = True
        self.key_position = pyautogui.locateCenterOnScreen(os.path.join(BASE_DIR, 'assets', 'OSK_{0}.png'.format(button)), grayscale=True)

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                pyautogui.mouseDown(self.key_position)
                time.sleep(self.delay)
            time.sleep(1)


click_thread = ClickMouse(0.1, 'c')
click_thread.start()


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
