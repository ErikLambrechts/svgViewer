from optparse import OptionParser
import sys
from PyQt5 import QtGui, QtSvg, QtWidgets, QtCore
import asyncore
import pyinotify

class ThreadClass(QtCore.QThread):

    def __init__(self, main):
        super().__init__()
        self.widget = main

    def run(self):
        # mask_events = pyinotify.IN_MODIFY

        # event handler
        eh = MyEventHandler(self.widget)

        wm = pyinotify.WatchManager()  # Watch Manager
        # notifier = pyinotify.AsyncNotifier(wm, lambda *args : ex.update(args))
        # notifier = pyinotify.AsyncNotifier(wm, test)
        # wdd = wm.add_watch('./', mask_events)
        wm.add_watch('./', pyinotify.ALL_EVENTS, rec=True)
        # notifier = pyinotify.Notifier(wm, eh)

        # notifier = pyinotify.AsyncNotifier(wm, eh)
        notifier = pyinotify.AsyncNotifier(wm, self.widget.reload())
        notifier.loop()

class MyEventHandler(pyinotify.ProcessEvent):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def process_IN_CREATE(self, event):
        self.widget.reload()

    def process_IN_MODIFY(self, event):
        self.widget.reload()

class Example(QtSvg.QSvgWidget):
    def __init__(self, name, parent):
        super().__init__(name)

        self.file_name = name
        self.parent = parent
        self.initUI()

    def reload(self):
        r = self.renderer().load(self.file_name)

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
        center = [x_center, y_center]
        self.parent.update(center = center)

    def keyPressEvent(self, QKeyEvent):
        print(QKeyEvent)
        if QKeyEvent.key() == QtCore.Qt.Key_R:
            self.parent.reload()
        if QKeyEvent.key() == QtCore.Qt.Key_Space:
            self.parent.reload()
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
             self.close()
        if QKeyEvent.key() == QtCore.Qt.Key_Plus:
            self.parent.update(scale_factor = 0.9)
        if QKeyEvent.key() == QtCore.Qt.Key_Minus:
            self.parent.update(scale_factor = 10/9)

    def mouseReleaseEvent(self, QMouseEvent):
        cursor =QtGui.QCursor()

    def update(self):
        dx_window = self.geometry().width()
        dy_window = self.geometry().height()

        dx_r= dx_window * self.parent.scale
        dy_r= dy_window * self.parent.scale

        r = QtCore.QRect(self.parent.center[0] - dx_r/2, self.parent.center[1] - dy_r/2, dx_r, dy_r)
        self.renderer().setViewBox(r)
        super().update()

    def initUI(self):
        svgWidget = QtSvg.QSvgWidget(self.file_name)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle(self.file_name)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

class main():
    def __init__(self):
        parser = OptionParser(usage="%prog files", version="%prog 1.0")
        # parser.add_option("-c", defougg
        (options, args) = parser.parse_args()
        app = QtWidgets.QApplication(sys.argv)
        svg_file = ['output_debug.svg', 'output_debug_selection.svg']
        svg_file = args
        self.windows = [Example(f, self) for f in svg_file]
        # watcher = ThreadClass(self)
        # watcher.start()
        self.center = [0,0]
        self.scale = 0.1

        for e in self.windows:
            e.show()

        sys.exit(app.exec_())

    def reload(self):
        for w in self.windows:
            w.reload()
        self.update()

    def update(self, center = None, scale=None, scale_factor = None):
        if center:
            self.center = center
        if scale:
            self.scale = scale
        if scale_factor:
            self.scale *= scale_factor

        for w in self.windows:
            w.update()

if __name__ == '__main__':
    m = main()

