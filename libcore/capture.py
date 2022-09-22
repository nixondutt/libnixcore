import io
import enum 
from queue import Full
from .job import Producer
from libcore.v4l2.video import Video, V4L2_PIX_FMT, VideoPort

class Frame(object):

    def __init__(self, value):
        self.value = value
        self.updatable = True

    def getvalue(self):
        self.updatable = False
        return self.value

    def _update(self, value):
        if self.updatable:
            self.value = value
            return True
        return False

class V4LCameraCapture(Producer):
    FormatSelector = enum.Enum("FormatSelector", "DEFAULT PROPER MAXIMUM")
    def __init__(self, device = '/dev/video0', size = (640, 480), framerate = 30,
                 expected_format = V4L2_PIX_FMT.RGB24, fallback_formats = (V4L2_PIX_FMT.YUYV,V4L2_PIX_FMT.MJPEG),
                 format_selector= FormatSelector.DEFAULT):
        super(V4LCameraCapture, self).__init__()
        self.video = Video(device)
        width, height = size
        if self.video.query_capability() == VideoPort.CSI:
            # workaround for bcm2835-v4l2 format pixsize & bytesperline bug
            width = (width+31) // 32 * 32
            height = (height +15) // 16 * 16
            
            #workaround for bcm2835-v4l2 IMX219 32*32 -> 800*800 capture timeout bug
            candidates = video.lookup_config(64,64,5, V4L2_PIX_FMT.RGB24, V4L2_PIX_FMT.RGB24)
            video.set_format(candidates[0],64,64,V4L2_PIX_FMT.RGB24)
        
        if format_selector in [V4LCameraCapture.FormatSelector.PROPER, V4LCameraCapture.FormatSelector.MAXIMUM]:

            def cmp(config):  # type: ignore
                return (
                    config.width * config.height,
                    config.height,
                    config.width,
                    config.interval.denominator / config.interval.numerator,
                )
        else:
            def cmp(config):
                return 1
        
        config =None
        fmts = [expected_format] + [f for f in fallback_formats]
        for fmt in fmts:
            expected_framerate = 1 if format_selector == V4LCameraCapture.FormatSelector.MAXIMUM else framerate
            candidates = self.video.lookup_config(width, height, expected_framerate, fmt, expected_format)
            candidates = sorted(candidates, key=cmp)
            if len(candidates) > 0:
                config = candidates[-1 if format_selector == V4LCameraCapture.FormatSelector.MAXIMUM else 0]
                break
        if config is None:
            raise RuntimeError("expected capture format is unsupported")
        if format_selector == V4LCameraCapture.FormatSelector.MAXIMUM:
            fmt = self.video.set_format(config, expected_format= expected_format)
        else:
            fmt = self.video.set_format(config, width, height, expected_format=expected_format)
        self.capture_width, self.capture_height, self.capture_format = fmt
        self.video.set_framerate(config)
        self.video.request_buffers(4)
        self.video.queue_buffer()

        self.frames = []
        # candidates = self.video.lookup_config(width, height, framerate, expected_format)
        # for fallback_format in fallback_formats:
        #     candidates += self.video.lookup_config(width, height, framerate, fallback_format)
        # config = candidates[0]
        # self.video.set_format(config, width, height, expected_format)
        # self.video.set_framerate(config)
        # # video.set_rotation(90)
        # buffers = self.video.request_buffers(4)
        # for buf in buffers:
        #     self.video.queue_buffer(buf)

    def run(self):

        with self.video.start_streaming() as stream:
            while self._is_running():
                try:
                    value = stream.capture(timeout = 5)
                    updated = 0
                    for frame in reversed(self.frames):
                        if frame._update(value):
                            updated += 1
                        else:
                            break
                    self.frames = self.frames[len(self.frames)-updated:]
                    frame = Frame(value)
                    if self._outlet(frame):
                        self.frames.append(frame)
                except:
                    raise

    def _outlet(self, o):
        length = len(self.out_queues)
        while self._is_running():
            try:
                self.out_queues[self.out_queue_id%length].put(o, block=False)
                self.out_queue_id += 1
                return True
            except Full:
                return False
            except:
                traceback.print_exc()
        return False