import time
from threading import RLock, Thread


class vs:
    def __init__(self):
        self.stream_url = 'rtsp://113.161.57.246:11555/user=admin_password=_channel=1_stream=0.sdp?real_stream'
        self.stt_lock = RLock()

    def start(self):
        check_url = check(self.stream_url)
        if check_url:
            with self.stt_lock:
                Thread(target=self._run).start()
        return check_url

    def _run(self):
        i = 0
        while True:
            i += 1
            print(i)
            time.sleep(1)


class cp:
    def __init__(self):
        self.dict_a = {}
        self.lock = RLock()

    def add(self, id):
        with self.lock:
            a = vs()
            self.dict_a[id] = a

    def start_b(self, id):
        return self.dict_a[id].start()


class bus:
    b = cp()

    @staticmethod
    def add_c(id):
        return bus.b.add(id)

    @staticmethod
    def start_c(id):
        return bus.b.start_b(id)


class AIFuncBus:
    @classmethod
    def start_process(cls):
        bus.add_c(1)
        return bus.start_c(1)


# must put these 2 function outside the class
# if they are put inside the VideoSource class, multiprocessing will throw exception "can't pickle _thread.RLock objects"
def check(stream_url, timeout=10):
    import multiprocessing

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    check_process = multiprocessing.Process(target=_try_check, args=(stream_url, return_dict,))

    check_process.start()
    check_process.join(timeout=timeout)
    check_process.terminate()

    return return_dict.get(stream_url, False)


def _try_check(stream_url, return_dict):
    # noinspection PyBroadException
    try:
        import cv2
        video = cv2.VideoCapture(stream_url)
        if not video.isOpened():
            return_dict[stream_url] = False
            return False
        grabbed = video.grab()
        return_dict[stream_url] = grabbed
        return grabbed

    except Exception:
        return_dict[stream_url] = False
        return False


if __name__ == '__main__':
    c = AIFuncBus.start_process()
    d = 1
