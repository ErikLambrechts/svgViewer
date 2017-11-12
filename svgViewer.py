import sys
from PyQt5 import QtGui, QtSvg, QtWidgets, QtCore
import asyncore
import pyinotify
from optparse import OptionParser

class ThreadClass(QtCore.QThread):

    def __init__(self, widgit):
        super().__init__()
        self.widget = widgit

    def run(self):
        mask_events = pyinotify.IN_MODIFY
        # event handler
        eh = MyEventHandler(self.widget)

        wm = pyinotify.WatchManager()  # Watch Manager
        # notifier = pyinotify.AsyncNotifier(wm, lambda *args : ex.update(args))
        # notifier = pyinotify.AsyncNotifier(wm, test)
        # wdd = wm.add_watch('./', mask_events)
        wm.add_watch('./', pyinotify.ALL_EVENTS, rec=True)
        # notifier = pyinotify.Notifier(wm, eh)
        notifier = pyinotify.AsyncNotifier(wm, eh)
        notifier.loop()

class Example(QtSvg.QSvgWidget):
    def __init__(self, name, parent = None):
        super().__init__(name)

        self.file_name = name
        self.initUI()
        self.parent = parent
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

        self.parent.update()

    def mouseReleaseEvent(self, QMouseEvent):
        cursor =QtGui.QCursor()

    def update(self):

        dx_window = self.geometry().width()
        dy_window = self.geometry().height()

        dx_r= dx_window * self.scale
        dy_r= dy_window * self.scale

        r = QtCore.QRect(self.center[0] - dx_r/2, self.center[1] - dy_r/2, dx_r, dy_r)
        self.renderer().setViewBox(r)
        super().update()

    def initUI(self):
        svgWidget = QtSvg.QSvgWidget(self.file_name)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('Quit button')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

class MyEventHandler(pyinotify.ProcessEvent):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def process_IN_CREATE(self, event):
        self.widget.update()

    def process_IN_MODIFY(self, event):
        self.widget.update()

class svgViewer(object):
    def __init__(self, filenames):
        print("init app")
        self.app = QtWidgets.QApplication(sys.argv)
        self.widgits = []
        for f in filenames:
            print("init widget " + f)
            self.widgits.append(Example(f))

        print("init watcher")
        self.watcher = ThreadClass(self)
        print("end init")

    def start(self):
        print("start watcher")
        self.watcher.start()
        for ex in self.widgits:
            print("start widgits")
            ex.show()

    def update(self):
        for ex in self.widgits:
            ex.update()

    def __del__(self):
        sys.exit(self.app.exec_())

def main():

    parser = OptionParser(usage="%prog files", version="%prog 1.0")
    (options, args) = parser.parse_args()

    # svgViewer(args)
    svg_viewer = svgViewer(['output_debug.svg'])
    print("main")
    svg_viewer.start()
    print("main")

if __name__ == '__main__':
    main()

