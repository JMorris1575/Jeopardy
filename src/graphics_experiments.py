# A program to facilitate experimentation with QGraphicsView, QGraphicsScene and QGraphicsItem and how they interact
# with their containers.

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time

class GraphicsTester(QMainWindow):

    def __init__(self, parent=None):
        super(GraphicsTester, self).__init__(parent)

        testMenu = self.menuBar().addMenu('&Tests')
        self.motion_action = testMenu.addAction('&Motion')
        self.motion_action.triggered.connect(self.MoveScene)
        self.zoom_in_action = testMenu.addAction('Zoom &In')
        self.zoom_in_action.triggered.connect(self.ZoomIn)
        self.zoom_out_action = testMenu.addAction('Zoom &Out')
        self.zoom_out_action.triggered.connect(self.ZoomOut)

        self.view = QGraphicsView()
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
        self.Setup()

    def MoveScene(self):
        increment = 310/49
        for i in range(50):
            self.view.setSceneRect(0 + increment * i, 0, 300, 200)
            time.sleep(0.0167)
            self.view.repaint()

    def ZoomIn(self):
        # increment = 1/49
        self.view.centerOn(3 * (150 + 10) + 75, 3 * (100 + 10) + 50)
        for i in range(25):
            self.view.resetTransform()
            zoom = 1 + (5 * i)/24
            print(zoom)
            self.view.scale(zoom, zoom)
            time.sleep(0.0167)
            self.view.repaint()

    def ZoomOut(self):
        # increment = 2/49
        # for i in range(50):
        #     self.view.scale(2 - increment, 2 - increment)
        #     time.sleep(0.0167)
        #     self.view.repaint()
        self.view.scale(0.333, 0.333)

    def Setup(self):
        redPen = QPen()
        redPen.setColor(Qt.red)
        redPen.setWidth(5)
        bluePen = QPen()
        bluePen.setColor(Qt.blue)
        bluePen.setWidth(5)
        for col in range(6):
            for row in range(6):
                rect = QGraphicsRectItem(0, 0, 150, 100)
                text = QGraphicsTextItem("(" + str(row) + ", " + str(col) + ")")
                if (col + row) % 2 == 0:
                    rect.setPen(bluePen)
                else:
                    rect.setPen(redPen)
                rect.setPos(col * (150 + 10), row * (100 + 10))
                text.setPos(col * (150 + 10) + 60, row * (100 + 10) + 40)
                self.scene.addItem(rect)
                self.scene.addItem(text)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('GraphicsTester')
    form = GraphicsTester()
    form.show()
    app.exec()
