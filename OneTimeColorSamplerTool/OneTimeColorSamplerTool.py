from krita import *
from krita import DockWidget
from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton, QSizePolicy, QMessageBox, QDialog

from PyQt5 import QtCore

DOCKER_TITLE = 'One-time Color Sampler Tool'

class OneTimeColorSamplerTool(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)

        self.baseWidget = QWidget()
        self.layout = QGridLayout()
        self.firstTimeRun = True
        self.colorPickActivated = False

        self.btncolorpicker = QToolButton()
        self.btncolorpicker.setStyleSheet("background-color:#000000;")
        self.btncolorpicker.setText("Col.\nPckr")
        self.btncolorpicker.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btncolorpicker.clicked.connect(lambda: Krita.instance().action('KritaSelected/KisToolColorSampler').trigger())
        self.btncolorpicker.clicked.connect(self.addMouseEventsToColorChange)
        self.layout.addWidget(self.btncolorpicker, 2, 2)
        
        self.baseWidget.setLayout(self.layout)
        self.setWidget(self.baseWidget)

    # notifies when views are added or removed
    # 'pass' means do not do anything
    def canvasChanged(self, canvas):
        pass

    def addMouseEventsToColorChange(self):
        qwin = Krita.instance().activeWindow().qwindow()
        self.addConsoleMessage("starting to inject myself to color changes")
        self.colorPickActivated = True

        if self.firstTimeRun:
            self.firstTimeRun = False
            mouse_observer = MouseObserver(qwin.windowHandle())

            #mouse_observer.pressed.connect(lambda pos: print(f"pressed: {pos}"))
            #mouse_observer.released.connect(lambda pos: print(f"released: {pos}"))
            #mouse_observer.moved.connect(lambda pos: print(f"moved: {pos}"))

            mouse_observer.released.connect(self.activateBrushOnMouseRelease)

    def addConsoleMessage(self, message):
        print(message)

    def activateBrushOnMouseRelease(self):
        if self.colorPickActivated:
            Krita.instance().action("KritaShape/KisToolBrush").trigger()
            self.colorPickActivated = False
            self.addConsoleMessage("Color has been chosen; Returning to Brush tool.")
        


class MouseObserver(QtCore.QObject):
    pressed = QtCore.pyqtSignal(QtCore.QPoint)
    released = QtCore.pyqtSignal(QtCore.QPoint)
    moved = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, window):
        super().__init__(window)
        self._window = window

        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window

    def eventFilter(self, obj, event):
        if self.window is obj:
            if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.TabletPress:
                self.pressed.emit(event.pos())
            elif event.type() == QtCore.QEvent.MouseMove or event.type() == QtCore.QEvent.TabletMove:
                self.moved.emit(event.pos())
            elif event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.TabletRelease:
                self.released.emit(event.pos())
        return super().eventFilter(obj, event)
