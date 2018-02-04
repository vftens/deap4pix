import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtCore import *

from PIL import Image


class HTMLRenderer(QWebView):
    def __init__(self):
        self.app = QApplication([])
        QWebView.__init__(self)
        self.resize(1024, 640)
        self.page().setViewportSize(self.size())

    def render_html(self, html):
        self.setHtml(html)
        frame = self.page().mainFrame()

        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        image = image.convertToFormat(QImage.Format_ARGB32)
        bytes = image.bits().asstring(image.byteCount())

        mode = "RGBA"
        pilimg = Image.frombuffer(mode, (image.width(), image.height()), bytes, 'raw', mode, 0, 1)
        # pilimg.show()

        # pilimg.save('test_render2.png')
        return pilimg


import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


def html2img(html):
    render = HTMLRenderer()
    return render.render_html(html)


# def html2img(html):
#     imgkit.from_string(html, 'tmp.png', options={'width': 1024, 'height': 640, 'quiet': ''})
#     return Image.open('tmp.png')


if __name__ == '__main__':
    html = open('dataset/markup.html').read()
    html2img(html)
