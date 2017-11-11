#!/usr/bin/python
import sys
from PyQt5 import QtGui, QtSvg, QtWidgets, QtCore
import asyncore
import pyinotify

from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
            print("Howdy!  Gig'em!  Whoop!")
            time.sleep(10)
# app = QtWidgets.QApplication(sys.argv)
# svgWidget = QtSvg.QSvgWidget('output_debug.svg')
# # svgWidget.setGeometry(50,50,759,668)
# svgWidget.show()

# sys.exit(app.exec_())
class Example(QtSvg.QSvgWidget):
    def __init__(self, name):
        super().__init__(name)
        self.file_name = name
        self.initUI()
        self.scale = 0.1
        self.center = [0, 0]

    def mousePressEvent(self, QMouseEvent):
        x_mouse = QMouseEvent.pos().x()
        y_mouse = QMouseEvent.pos().y()
        x_window = self.geometry().x()
        y_window = self.geometry().y()
        vb = self.renderer().viewBox()
        dx_window = self.geometry().width()
        dy_window = self.geometry().height()
        x_center = (x_mouse - x_window) / dx_window * vb.width() + vb.x()
        y_center = (y_mouse - y_window) / dy_window * vb.height() + vb.y()
        self.center = [x_center, y_center]
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        cursor =QtGui.QCursor()
        print( cursor.pos())

    def update(self, a = None):
        print("a : ", a)

        dx_window = self.geometry().width()
        dy_window = self.geometry().height()

        dx_r= dx_window * self.scale
        dy_r= dy_window * self.scale

        r = QtCore.QRect(self.center[0] - dx_r/2, self.center[1] - dy_r/2, dx_r, dy_r)
        self.renderer().setViewBox(r)
        super().update()

    def initUI(self):
        svgWidget = QtSvg.QSvgWidget(self.file_name)
        # qbtn = QtGui.QPushButton('Quit', self)
        # qbtn.resize(qbtn.sizeHint())
        # qbtn.move(50, 50)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('Quit button')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.show()

    # def run(self):
    #     self.show()

    def test(self):
        print( "test")

def main():
    # app = QtWidgets.QApplication(sys.argv)
    # svg_file = 'output_debug.svg'
    # ex = Example(svg_file)

    # wm = pyinotify.WatchManager()  # Watch Manager
    # mask_events = pyinotify.IN_MODIFY

    # # ex.update()
    # notifier = pyinotify.AsyncNotifier(wm, lambda *args : ex.update(args))
    # wdd = wm.add_watch('./', mask_events)

    # sys.exit(app.exec_())

    app = App()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()

if __name__ == '__main__':
    main()
# asyncore.loop()
# svgWidget.setGeometry(50,50,759,668)

