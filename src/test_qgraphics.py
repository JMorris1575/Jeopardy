from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TestItem(QGraphicsItem):

    def __init__(self, id, size, controller, font=None, color=QColor(Qt.white), text="", parent=None):
        super(TestItem, self).__init__(parent)
        self.id = id
        self.controller = controller
        # self.position = pos
        self.size = size

        self.font = font
        self.color = color

        self.text = text
        self._shadow_text = QGraphicsTextItem(self.text, self)
        self._shadow_text.setDefaultTextColor(QColor(Qt.black))
        self._text_item = QGraphicsTextItem(self.text, self)
        self._text_item.setDefaultTextColor(QColor(self.color))

    def __str__(self):
        return self.id

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        target = QRectF(self.boundingRect())
        pixmap = QPixmap('../images/blue_screen.png')
        source = QRectF(pixmap.rect())
        painter.drawPixmap(target, pixmap, source)
        self.formatText()

    def formatText(self):
        """
        Adjusts self._text_item and self._shadow_text to display as a shadowed font.
        :return: None
        """
        self.font.setCapitalization(QFont.AllUppercase)
        font_metrics = QFontMetrics(self.font)
        self._shadow_text.setPlainText(self.text)
        self._shadow_text.setFont(self.font)
        self._shadow_text = self.centerText(self._shadow_text,)
        shadow_offset = font_metrics.capHeight() * 0.07
        self._shadow_text.moveBy(shadow_offset, shadow_offset)

        self._text_item.setPlainText(self.text)
        self._text_item.setFont(self.font)
        self._text_item = self.centerText(self._text_item)                # foreground is not offset

    def centerText(self, graphics_text_item):

        # Center alignment code adapted from http://www.cesarbs.org/blog/2011/05/30/aligning-text-in-qgraphicstextitem/

        format_block = QTextBlockFormat()
        format_block.setAlignment(Qt.AlignCenter)
        graphics_text_item.setFont(self.font)
        graphics_text_item.setTextWidth((self.size.width() * 0.97))  # leave some padding
        cursor = graphics_text_item.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(format_block)
        cursor.clearSelection()
        graphics_text_item.setTextCursor(cursor)

        # That worked! Now for the vertical centering

        y_offset = (self.size.height() - graphics_text_item.boundingRect().height())/2

        shadow_offset = self.size.width() * .01
        graphics_text_item.setPos(shadow_offset, shadow_offset + y_offset)
        graphics_text_item.setPos(0.0, y_offset)

        graphics_text_item.setPos(0, y_offset)

        return graphics_text_item

    def mousePressEvent(self, event):
        self.controller.processMousePress(self, event)


class TestQGraphics(QMainWindow):

    def __init__(self, parent=None):
        super(TestQGraphics, self).__init__(parent)

        self.category_font = QFont("Arial", 36)
        self.clue_font = QFont("Times New Roman", 18)
        self.number_font = QFont("Arial", 32, QFont.Bold)

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        item_one = TestItem("Item One", QSizeF(400, 225), self, font=self.category_font)
        item_one.setPos(QPointF(10, 10))
        item_two = TestItem("Item Two", QSizeF(200, 112.5), self, font=self.category_font)
        item_two.setPos(QPointF(10, item_one.size.height() + 20))
        item_one.font = self.category_font
        item_one.text = "This is some sample text."
        item_one.color = QColor(Qt.white)
        item_two.font = self.clue_font
        item_two.text = "This is some more sample text."
        item_two.color = QColor(Qt.white)
        self.scene.addItem(item_one)
        self.scene.addItem(item_two)
        self.view.setSceneRect(self.scene.itemsBoundingRect())

        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate) #todo: find out what this does

        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.count = 0

    def processMousePress(self, display, event):
        print(display.id + " received a mousePressEvent.")
        display.text = str(self.count)
        self.count += 1
        print("len(self.scene.items()) = ", len(self.scene.items()))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('QGraphics Practice Program')
    form = TestQGraphics()
    form.show()
    app.exec()
