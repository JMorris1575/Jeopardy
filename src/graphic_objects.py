from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import *


class DisplayUnit(QGraphicsItem):

    def __init__(self, size, type, controller, parent=None):
        super(DisplayUnit, self).__init__(parent)
        self.size = size
        self.type = type                # either DisplayType.Category or DisplayType.Clue
        self.controller = controller

        self.displayed_text = ""    # the text that will be displayed
        self.text_A = ""            # text_A is the main thing to display: category name or clue
        self.text_B = ""            # text_B is the secondary thing to display: category explanation or correct response
        self._shadow_text = QGraphicsTextItem(self.displayed_text, self)
        self._shadow_text.setDefaultTextColor(QColor(Qt.black))
        self._text_item = QGraphicsTextItem(self.displayed_text, self)      # color to be set in displayText()
        # self._text_item.setDefaultTextColor(QColor(self.color))

        # self.setFlags(Qt.ItemIsSelectable | Qt.Focusable)
        self._text_item.setTextInteractionFlags(Qt.NoTextInteraction)

        if self.type == DisplayType.Category:
            self.font = self.controller.category_font
            self._text_item.setDefaultTextColor(QColor(Qt.white))

        #:todo: figure out how to handle the following three things in this new approach
        self.setDisplayState(DisplayState.Blank)
        # self.hide_category = False
        # self.category_cover = QPixmap('../images/jeopardy.png')

    # The following two methods are mandatory when subclassing QGraphicsItem

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    # def paint(self, painter, option, widget):
    #     target = QRectF(self.boundingRect())
    #     if self.hide_category:
    #         pixmap = self.category_cover
    #         source = QRectF(pixmap.rect())
    #         painter.drawPixmap(target, pixmap, source)
    #     else:
    #         pixmap = QPixmap('../images/blue_screen.png')
    #         source = QRectF(pixmap.rect())
    #         painter.drawPixmap(target, pixmap, source)
    #         self.displayText()

    def paint(self, painter, option, widget):
        target = QRectF(self.boundingRect())
        pixmap = QPixmap('../images/blue_screen.png')
        source = QRectF(pixmap.rect())
        painter.drawPixmap(target, pixmap, source)
        self.formatText()

    # Here is where my own methods start

    def setDisplayState(self, state):
        """
        Sets the display state of the unit by setting its font and color
        :param state: the DisplayState of the unit
        :return: None
        """
        # first set the new display_state
        self.display_state = state

        # now deal with the fonts and colors of the clue units
        if self.type == DisplayType.Clue:
            if self.display_state == DisplayState.Dollars or self.display_state == DisplayState.Points:
                self._text_item.setDefaultTextColor(QColor(Qt.yellow))
                self.font = self.controller.number_font
            else:
                self._text_item.setDefaultTextColor(QColor(Qt.white))
                self.font = self.controller.clue_font

        # finally deal with what should be displayed
        if self.display_state == DisplayState.Blank:
            self.displayed_text = ''
        elif self.display_state == DisplayState.Waiting:
            self.displayed_text = '?'
        elif self.display_state == DisplayState.A_Text:
            self.displayed_text = self.text_A
        elif self.display_state == DisplayState.B_Text:
            self.displayed_text = self.text_B
        elif self.display_state == DisplayState.Dollars:
            self.displayed_text = '$' + str(self.amount)
        elif self.display_state == DisplayState.Points:
            self.displayed_text = str(self.amount)
        else:
            print("A DisplayState was entered that does not exist. (This should be an exception.)")

    def formatText(self):
        """
        Adjusts self._text_item and self._shadow_text to display as a shadowed font.
        :return: None
        """
        self.font.setCapitalization(QFont.AllUppercase)
        font_metrics = QFontMetrics(self.font)
        self._shadow_text.setPlainText(self.displayed_text)
        self._shadow_text.setFont(self.font)
        self._shadow_text = self.centerText(self._shadow_text,)
        shadow_offset = font_metrics.capHeight() * 0.07
        self._shadow_text.moveBy(shadow_offset, shadow_offset)

        self._text_item.setPlainText(self.displayed_text)
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
        button = event.button()
        self.controller.mousePressProcessing(self, button)
