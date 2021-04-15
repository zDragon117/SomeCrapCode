import numpy as np
import cv2
import os
from shutil import move

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def move_file(src: str, dst: str):
    result = False
    if os.path.exists(src):
        try:
            move(src, dst)
            result = True
        except:
            pass
    return result


def delete_file(path: str):
    result = False
    if os.path.exists(path):
        try:
            os.remove(path)
            result = True
        except:
            pass
    return result


def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    # h_min = min(im.shape[0] for im in im_list)
    h_min = 360
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation) for im in im_list]
    return cv2.hconcat(im_list_resize)


def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation) for im in im_list]
    return cv2.vconcat(im_list_resize)


def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=interpolation) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=interpolation)


def combine_video(arrVideo, fps, outputPath):
    print('Combine Video Start')
    outputPathTemp = os.path.splitext(outputPath)[0] + '_tmp' + '.mp4'
    arrCapVideo = {}
    for key, value in arrVideo.items():
        print(key)
        print(value)
        arrCapVideo[key] = {}
        arrCapVideo[key]['cap'] = cv2.VideoCapture(value, 0)
        arrCapVideo[key]['old_ret'] = None
        arrCapVideo[key]['old_frame'] = None
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    outVideoWriter = None
    black_frame = np.zeros((360, 480, 3), np.uint8)
    while True:
        notOver = False
        frames = {}
        for key, value in arrCapVideo.items():
            ret, frame = arrCapVideo[key]['cap'].read()
            if not ret: frame = arrCapVideo[key]['old_frame']
            arrCapVideo[key]['old_ret'] = ret
            arrCapVideo[key]['old_frame'] = frame
            frames[key] = frame
            notOver = notOver or ret
        if not notOver: break
        videoFrame = concat_tile_resize([[frames['FRONT'], frames['BACK']]])
        if not outVideoWriter:
            outVideoWriter = cv2.VideoWriter(outputPathTemp, fourcc, fps, (videoFrame.shape[1], videoFrame.shape[0]))
        outVideoWriter.write(videoFrame)
    for key, value in arrCapVideo.items():
        arrCapVideo[key]['cap'].release()
    if outVideoWriter:
        outVideoWriter.release()
    delete_file(outputPath)
    move_file(outputPathTemp, outputPath)
    print('Combine Video End')


if __name__ == '__main__':
    file_path = BASE_DIR + '/test.mp4'
    filesConvert = {
        'FRONT': BASE_DIR + '/FRONT.mp4',
        'BACK': BASE_DIR + '/BACK.mp4',
    }
    combine_video(filesConvert, 15, file_path)
