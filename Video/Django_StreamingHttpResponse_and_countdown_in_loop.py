globalIsOver = False


def gen_camera_stream_resp(
        camera_source,
        fps=10,
        scale_width=720,
        scale_height=-1,
):
    countdown(120)
    while True and not over():
        try:
            frame = camera_source.get_stream_data(
                scale_width=scale_width,
                scale_height=scale_height,
            ).tobytes()
            yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
            )
            time.sleep(float(1) / fps)

        except Exception:
            time.sleep(0.3)
            break


def countdown(time):
    t = Timer(time, set_over)
    t.start()


def set_over():
    global globalIsOver
    globalIsOver = True


def over():
    return globalIsOver


@gzip.gzip_page
@api_view(['GET'])
def live_stream(request, camera_id):
    try:
        global globalIsOver
        globalIsOver = False

        fps = int(request.GET.get('fps', 10))
        scale_width = int(request.GET.get('scale_width', 720))
        scale_height = int(request.GET.get('scale_height', -1))

        camera_source = AlarmBus.get_worker(camera_id).get_video_source()

        return StreamingHttpResponse(
            gen_camera_stream_resp(
                camera_source,
                fps=fps,
                scale_width=scale_width,
                scale_height=scale_height,
            ),
            content_type='multipart/x-mixed-replace;boundary=frame',
        )

    except Exception as exc:
        return JsonResponse({
            'Error': f'Bad Request: {exc}'
        }, status=400)