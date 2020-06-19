import os
import platform
import time
import datetime
from threading import Thread

import cv2
import argparse
import imutils

# # Create the parser
# my_parser = argparse.ArgumentParser()

# # Add the arguments
# my_parser.add_argument('-r',
#                        '--rtsp',
#                        required=True,
#                        help='RTSP link.')

# my_parser.add_argument('-d',
#                        '--dest',
#                        required=True,
#                        help='RTSP link.')

# # Execute the parse_args() method
# args = my_parser.parse_args()

video = None
frame = None
grabbed = False
is_record = True
is_get_frame = True
_OS = platform.system()
_FourCC = cv2.VideoWriter_fourcc(*'DIVX') if _OS == 'Windows' else cv2.VideoWriter_fourcc(*'XVID')


def loop_get_frame():
    global frame, grabbed, is_record, is_change_lap
    while is_get_frame:
        start_time = time.time()
        grabbed, frame = video.read()
        frame = scale_frame(frame, 960, -1)
        try:
            fps = 1/(time.time() - start_time)
        except ZeroDivisionError:
            pass
        draw_fps(frame, fps)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            is_record = False
            break

    video.release()
    cv2.destroyAllWindows()


def record_frame(destination):
    global is_change_lap
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    src_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    src_fps = video.get(cv2.CAP_PROP_FPS)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    dest_video = cv2.VideoWriter(destination + "sample_in_out_" + now + ".mp4", _FourCC, src_fps, (src_width, src_height))

    while is_record:
        dest_video.write(frame)

    dest_video.release()


def scale_frame(frame, scale_width, scale_height):
    if scale_width != -1:
        if scale_height != -1:
            frame = cv2.resize(frame, (scale_width, scale_height))
        else:
            frame = imutils.resize(frame, width=scale_width)
    elif scale_height != -1:
        frame = imutils.resize(frame, height=scale_height)
    return frame


def draw_fps(frame, fps):
    font_scale = 0.5
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'fps: {:.1f}'.format(fps)
    (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
    text_offset_x = 10
    text_offset_y = 20
    cv2.rectangle(
        frame,
        (text_offset_x - 1, text_offset_y - text_height),
        (text_offset_x + text_width, text_offset_y + 5),
        (0, 0, 0),
        cv2.FILLED,
    )
    cv2.putText(
        frame, text, (text_offset_x, text_offset_y),
        font, fontScale=font_scale, color=(255, 255, 255), thickness=1,
    )

    return frame


class A:
    rtsp = 'rtsp://3.kizuna.vn:3556/user=rtsp2_password=admin123_channel=1_stream=0.sdp?real_stream'
    dest = 'C:\\Projects\\Zet\\SomeCrapCode\\Video\\sample\\'


if __name__ == '__main__':
    args = A()
    video = cv2.VideoCapture(args.rtsp)
    print(f'VideoSource [{args.rtsp}] connect successfully!')
    dest = args.dest
    print(dest)
    print(f'VideoSource [{args.rtsp}] begin getting frame!')
    Thread(target=loop_get_frame).start()
    time.sleep(5)
    print(f'VideoSource [{args.rtsp}] begin recording frame!')
    Thread(target=record_frame, args=(dest,)).start()
