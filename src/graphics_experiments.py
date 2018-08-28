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

        self.view = QGraphicsView()
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene()
        redPen = QPen()
        redPen.setColor(Qt.red)
        redPen.setWidth(5)
        self.rect = QGraphicsRectItem()
        self.rect.setPen(redPen)
        self.rect.setRect(0, 0, 300, 200)
        self.rect02 = QGraphicsRectItem(310, 0, 300, 200)
        bluePen = QPen()
        bluePen.setColor(Qt.blue)
        bluePen.setWidth(5)
        self.rect02.setPen(bluePen)
        self.scene.addItem(self.rect)
        self.scene.addItem((self.rect02))
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
        self.view.setSceneRect(-10, -10, 320, 220)

    def MoveScene(self):
        increment = 310/49
        for i in range(50):
            self.view.setSceneRect(0 + increment * i, 0, 300, 200)
            time.sleep(0.0167)
            self.view.repaint()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('GraphicsTester')
    form = GraphicsTester()
    form.show()
    app.exec()
