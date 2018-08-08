from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class BoardScreen(QGraphicsItem):

    def __init__(self, size):
        super(BoardScreen, self).__init__()
        self.size = size
        self.black_text = QGraphicsTextItem("This is centered.", self)
        self.black_text.setFont((QFont('Arial', 18)))
        self.black_text.setTextWidth(size.width() - size.width() * .03)
        self.black_text.setDefaultTextColor(QColor(Qt.black))
        self.text = QGraphicsTextItem("This is centered.", self)
        # self.text.setPlainText("This is a QGraphics TextItem.")
        self.text.setFont(QFont('Arial', 18))
        self.text.setTextWidth(size.width() - size.width() * .03)
        self.text.setDefaultTextColor(QColor(Qt.white))

        # Center alignment code adapted from http://www.cesarbs.org/blog/2011/05/30/aligning-text-in-qgraphicstextitem/

        format = QTextBlockFormat()
        format.setAlignment(Qt.AlignCenter)
        cursor = self.black_text.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(format)
        cursor.clearSelection()
        self.black_text.setTextCursor(cursor)
        cursor = self.text.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(format)
        cursor.clearSelection()
        self.text.setTextCursor(cursor)

        # That worked! Now for the vertical centering
        y_offset = (self.size.height() - self.text.boundingRect().height())/2
        shadow_offset = self.size.width() * .01
        self.black_text.setPos(shadow_offset, shadow_offset + y_offset)
        self.text.setPos(0.0, y_offset)

        print("self.text.boundingRect() = ", self.text.boundingRect())

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        target = QRectF(self.boundingRect())
        pixmap = QPixmap('../images/blue_screen.png')
        source = QRectF(pixmap.rect())
        painter.drawPixmap(target, pixmap, source)
        #self.text.paint(painter, QStyleOptionGraphicsItem(), widget)
