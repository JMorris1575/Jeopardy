from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import *


class DisplayUnit(QGraphicsItem):

    def __init__(self, size, type=None, category_text=None, category_explanation=None, amount=0,
                 clue=None, correct_response=None, parent=None):
        super(DisplayUnit, self).__init__(parent)
        self.size = size
        self.type = type
        self.category_text = category_text
        self.category_explanation = category_explanation
        self.amount = amount
        self.clue = clue
        self.correct_response = correct_response

        self.display_state = DisplayState.Blank

        self.category_font = QFont("Arial", 18)
        self.clue_font = QFont("Arial", 18)
        self.number_font = QFont("Arial", 40, QFont.Bold)

        self._shadow_text = QGraphicsTextItem(self)
        self._shadow_text.setDefaultTextColor(QColor(Qt.black))

        self._foreground_text = QGraphicsTextItem(self)     # the color will be set later in self.displayText()

    # The following two methods are mandatory when subclassing QGraphicsItem

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        target = QRectF(self.boundingRect())
        pixmap = QPixmap('../images/blue_screen.png')
        source = QRectF(pixmap.rect())
        painter.drawPixmap(target, pixmap, source)
        self.displayText()

    # Here is where my own methods start

    def displayText(self):
        """
        Prepares to set text in the DisplayUnit according to self.display_state
        :return: None
        """
        self._foreground_text.setDefaultTextColor(QColor(Qt.white))

        if self.display_state == DisplayState.Blank:
            self.formatText('', self.clue_font)                             # clear the text from the unit
        elif self.display_state == DisplayState.Waiting:
            self.formatText('?', self.number_font)
        elif self.display_state == DisplayState.Category:
            self.formatText(self.category_text, self.category_font)
        elif self.display_state == DisplayState.Explanation:
            self.formatText(self.category_explanation, self.category_font)
        elif self.display_state == DisplayState.Clue:
            self.formatText(self.clue, self.clue_font)
        elif self.display_state == DisplayState.Response:
            self.formatText(self.correct_response, self.clue_font)
        elif self.display_state == DisplayState.Dollars:
            self._foreground_text.setDefaultTextColor(QColor(Qt.yellow))
            self.formatText('$' + str(self.amount), self.number_font)
        elif self.display_state == DisplayState.Points:
            self.formatText(str(self.amount), self.number_font)
        else:
            print("A DisplayState was entered that does not exist. (This should be an exception.)")

    def formatText(self, text, font):
        """
        Adjusts self._foreground_text and self._shadow_text to display as a shadowed font.
        :param text: a String - the text to be adjusted
        :param font: the font to be used for this text
        :return:
        """

        self._shadow_text.setPlainText(text)
        self._shadow_text = self.centerText(self._shadow_text, font)
        shadow_offset = self.size.width() * 0.01
        self._shadow_text.moveBy(shadow_offset, shadow_offset)

        self._foreground_text.setPlainText(text)
        self._foreground_text = self.centerText(self._foreground_text, font)                # foreground is not offset


    def centerText(self, graphics_text_item, font):

        # Center alignment code adapted from http://www.cesarbs.org/blog/2011/05/30/aligning-text-in-qgraphicstextitem/

        format = QTextBlockFormat()
        format.setAlignment(Qt.AlignCenter)
        graphics_text_item.setFont(font)
        graphics_text_item.setTextWidth((self.size.width() * .97)) # leave some padding
        cursor = graphics_text_item.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(format)
        cursor.clearSelection()
        graphics_text_item.setTextCursor(cursor)

        # That worked! Now for the vertical centering

        y_offset = (self.size.height() - graphics_text_item.boundingRect().height())/2
        shadow_offset = self.size.width() * .01
        graphics_text_item.setPos(shadow_offset, shadow_offset + y_offset)
        graphics_text_item.setPos(0.0, y_offset)

        graphics_text_item.setPos(0, y_offset)

        return graphics_text_item


