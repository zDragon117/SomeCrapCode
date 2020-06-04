import datetime
import os
import platform
import time
from threading import Thread

import cv2
import argparse

# Create the parser
# my_parser = argparse.ArgumentParser()

# Add the arguments
# my_parser.add_argument('-r',
#                        '--rtsp',
#                        required=True,
#                        help='RTSP link.')

# my_parser.add_argument('-d',
#                        '--dest',
#                        required=True,
#                        help='RTSP link.')

# Execute the parse_args() method
# args = my_parser.parse_args()

video = None
frame = None
grabbed = False
is_get_frame = True


def loop_get_frame(destination):
    global frame, grabbed, is_record
    while is_get_frame:
        grabbed, frame = video.read()
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        file_path = os.path.join(destination, f'{now}.jpg')
        time.sleep(0.1)
        cv2.imwrite(file_path, frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            is_record = False
            break

    video.release()
    cv2.destroyAllWindows()


class A:
    rtsp = ''
    dest = 'images'


if __name__ == '__main__':
    args = A()
    video = cv2.VideoCapture(args.rtsp)
    os.makedirs(args.dest, exist_ok=True)
    Thread(target=loop_get_frame, args=(args.dest,)).start()
