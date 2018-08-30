# A program to facilitate experimentation with QGraphicsView, QGraphicsScene and QGraphicsItem and how they interact
# with their containers.

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time

class ZoomDialog(QDialog):

    def __init__(self, parent=None):
        super(ZoomDialog, self).__init__(parent)

        colLabel = QLabel("Column:")
        colSpin = QSpinBox()
        colSpin.setMaximum(5)
        colLabel.setBuddy(colSpin)
        colLabel.setAlignment(Qt.AlignRight)

        rowLabel = QLabel("Row:")
        rowSpin = QSpinBox()
        rowSpin.setMaximum(5)
        rowLabel.setBuddy(rowSpin)
        rowLabel.setAlignment(Qt.AlignRight)

        zoomButton = QPushButton("Zoom")
        zoomButton.click.connect(self.zoom_click)

        exitButton = QPushButton("Exit")
        exitButton.click.connect(self.exit_click)

        layout = QGridLayout()
        layout.addItem(colLabel, 0, 0)
        layout.addItem(colSpin, 0, 1)
        layout.addItem(rowLabel, 1, 0)
        layout.addItem(rowSpin, 1, 1)
        layout.addItem(zoomButton, 2, 0)
        layout.addItem(exitButton, 2, 1)

    def zoom_click(self):
        print("Got to zoom_click().")

    def exit_click(self):
        print("Got to exit_click().")

        self.setLayout(layout)

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

    def coords(self, col, row):
        return QPointF(col * 160, row * 110)

    def MoveScene(self):
        increment = 310/49
        for i in range(50):
            self.view.setSceneRect(0 + increment * i, 0, 300, 200)
            time.sleep(0.0167)
            self.view.repaint()

    def ZoomIn(self):
        self.view.centerOn(3 * 160 + 75, 4 * 110 + 50)
        for i in range(25):
            self.view.resetTransform()
            zoom = 1 + (5 * i)/24
            print(zoom)
            self.view.scale(zoom, zoom)
            time.sleep(0.0167)
            self.view.repaint()
        pos = self.coords(3,2)
        size = QSizeF(150, 100)
        print(pos + QPointF(size.width()/2, size.height()/2))

    def clickZoom(self, col, row):
        self.view.centerOn(col * 160 + 75, row * 110 + 50)
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
        self.view.scale(0.167, 0.167)

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
                rect.setPos(self.coords(col, row))
                text.setPos(col * (150 + 10) + 60, row * (100 + 10) + 40)
                self.scene.addItem(rect)
                self.scene.addItem(text)

    def mousePressEvent(self, event):
        print("Got to mousePressEvent with event = ", event)
        x = event.x()
        y = event.y()
        col = int(x/165)
        row = int(y/115)
        self.clickZoom(col, row)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('GraphicsTester')
    form = GraphicsTester()
    form.show()
    app.exec()
