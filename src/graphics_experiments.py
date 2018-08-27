# A program to facilitate experimentation with QGraphicsView, QGraphicsScene and QGraphicsItem and how they interact
# with their containers.

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class GraphicsTester(QMainWindow):

    def __init__(self, parent=None):
        super(GraphicsTester, self).__init__(parent)

        fakeMenu = self.menuBar().addMenu('&Fake Item')

        self.view = QGraphicsView()
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene()
        newPen = QPen()
        newPen.setColor(Qt.red)
        newPen.setWidth(5)
        self.rect = QGraphicsRectItem()
        self.rect.setPen(newPen)
        self.rect.setRect(0, 0, 300, 200)
        self.scene.addItem(self.rect)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)
        self.view.setSceneRect(-10, -10, 320, 220)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('GraphicsTester')
    form = GraphicsTester()
    form.show()
    app.exec()
