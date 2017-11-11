import sys
from PyQt5 import QtGui, QtSvg, QtWidgets, QtCore
import asyncore
import pyinotify

# app = QtWidgets.QApplication(sys.argv)
# svgWidget = QtSvg.QSvgWidget('output_debug.svg')
# # svgWidget.setGeometry(50,50,759,668)
# svgWidget.show()

class ThreadClass(QtCore.QThread):

    def __init__(self, widgit):
        super().__init__()
        self.widget = widgit

    # def run(self):
        # while True:
        #     time.sleep(1)
        #     print(1)

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
        # qbtn = QtGui.QPushButton('Quit', self)
        # qbtn.resize(qbtn.sizeHint())
        # qbtn.move(50, 50)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('Quit button')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        print("pre")
        print("post")

class MyEventHandler(pyinotify.ProcessEvent):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    # def process_IN_ACCESS(self, event):
    #     print("ACCESS event:", event.pathname)

    # def process_IN_ATTRIB(self, event):
    #     # print("ATTRIB event:", event.pathname)

    # def process_IN_CLOSE_NOWRITE(self, event):
    #     print("CLOSE_NOWRITE event:", event.pathname)

    # def process_IN_CLOSE_WRITE(self, event):
    #     print("CLOSE_WRITE event:", event.pathname)

    # def process_IN_CREATE(self, event):
    #     print("CREATE event:", event.pathname)

    # def process_IN_DELETE(self, event):
    #     print("DELETE event:", event.pathname)
    def process_IN_CREATE(self, event):
        self.widget.update()

    def process_IN_MODIFY(self, event):
        print( "MODIFY event:", event.pathname)

    # def process_IN_OPEN(self, event):
    #     print("OPEN event:", event.pathname)
        self.widget.update()

def main():
    app = QtWidgets.QApplication(sys.argv)
    svg_file = 'output_debug.svg'
    ex = Example(svg_file)
    watcher = ThreadClass(ex)
    watcher.start()

    ex.show()
    print("post sys")

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
# asyncore.loop()
# svgWidget.setGeometry(50,50,759,668)

