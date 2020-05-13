import os
import platform
import time
from threading import Thread

import cv2
import argparse

# Create the parser
my_parser = argparse.ArgumentParser()

# Add the arguments
my_parser.add_argument('-r',
                       '--rtsp',
                       required=True,
                       help='RTSP link.')

my_parser.add_argument('-d',
                       '--dest',
                       required=True,
                       help='RTSP link.')

# Execute the parse_args() method
args = my_parser.parse_args()

video = None
frame = None
grabbed = False
is_record = True
is_get_frame = True
_OS = platform.system()
_FourCC = cv2.VideoWriter_fourcc(*'DIVX') if _OS == 'Windows' else cv2.VideoWriter_fourcc(*'XVID')


def loop_get_frame():
    global frame, grabbed, is_record
    while is_get_frame:
        grabbed, frame = video.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            is_record = False
            break

    video.release()
    cv2.destroyAllWindows()


def record_frame(destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    src_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    src_fps = video.get(cv2.CAP_PROP_FPS)
    dest_video = cv2.VideoWriter(
        destination, _FourCC, 24, (src_width, src_height)
    )

    while is_record:
        print(frame)
        dest_video.write(frame.astype('uint8'))

    dest_video.release()


# class A:
#     rtsp = ''
#     dest = ''


if __name__ == '__main__':
    # args = A()
    video = cv2.VideoCapture(args.rtsp)
    print(f'VideoSource [{args.rtsp}] connect successfully!')
    dest = args.dest
    print(f'VideoSource [{args.rtsp}] begin getting frame!')
    Thread(target=loop_get_frame).start()
    time.sleep(5)
    print(f'VideoSource [{args.rtsp}] begin recording frame!')
    Thread(target=record_frame, args=(dest,)).start()
