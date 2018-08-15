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
        self.hide_category = False
        self.category_cover = QPixmap('../images/jeopardy.png')

        self.category_font = QFont("Arial", 18)
        self.clue_font = QFont("Arial", 18)
        self.number_font = QFont("Arial", 32, QFont.Bold)

        self._shadow_text = QGraphicsTextItem(self)
        self._shadow_text.setDefaultTextColor(QColor(Qt.black))

        self._foreground_text = QGraphicsTextItem(self)     # the color will be set later in self.displayText()

    # The following two methods are mandatory when subclassing QGraphicsItem

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        target = QRectF(self.boundingRect())
        if self.hide_category:
            pixmap = self.category_cover
            source = QRectF(pixmap.rect())
            painter.drawPixmap(target, pixmap, source)
        else:
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


class Board(QGraphicsItem):

    def __init__(self, screenGeometry, scene, parent=None):

        super(Board, self).__init__(parent)

        self.base_amount = 200                  # the smallest number of dollars or points
                                                # by using this variable you can opt to change it later
        # compute the size of the DisplayUnits
        display_unit_width = screenGeometry.width() * 0.1  # calculates 10% of the available height
        display_unit_height = display_unit_width * 9/16       # maintain a 16:9 aspect ratio
        display_unit_size = QSizeF(display_unit_width, display_unit_height)

        self.createBoard(display_unit_size, scene)

    # The following two methods are mandatory when subclassing QGraphicsItem

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        # paints all of the DisplayUnits in their current state
        print("In Board.paint()")
        for element in self.category_displays:
            print("Painting a category display")
            element.paint(painter, option, widget)
        for column in self.clue_displays:
            print("Painting a clue display")
            for element in column:
                element.paint(painter, option, widget)

    def createBoard(self, size, scene):
        """
        Creates a blank Jeopardy board for later use
        :param size: QFSize telling the width and height of the display units for this screen
        :return: None
        """
        # calculate the gap between display units (5% of the width of the unit)
        gap = size.width()/20

        # Create the category displays
        self.category_displays = []
        for col in range(6):
            element = DisplayUnit(size, type=DisplayType.Category)
            element.setPos(col * (size.width() + gap), 0)
            element.display_state = DisplayState.Blank
            self.category_displays.append(element)
            scene.addItem(element)

        # Create the clue displays
        self.clue_displays = []
        for col in range(6):
            row_list = []
            for row in range(5):
                element = DisplayUnit(size, DisplayType.Clue)
                element.setPos(col * (size.width() + gap), size.height() + 2 * gap + row * (size.height() + gap))
                element.display_state = DisplayState.Blank
                scene.addItem(element)
                row_list.append(element)
            self.clue_displays.append(row_list)

    def fillBoard(self, game, segment):
        """
        Fills all of the Category and Clue units
        :param game: an instance of the Game class
        :param segment: a member of the Segment class: Segment.Jeopardy, Segment.DoubleJeopardy or Segment.FinalJeopardy
        :return: None
        """
        if segment == Segment.Jeopardy or segment == Segment.DoubleJeopardy:
            categories = game.get_categories(segment)
            col = 0
            for category in categories:
                self.category_displays[col].category_text = category.title
                self.category_displays[col].category_explanation = category.explanation
                # the following line is temporary. Later it should display a "Jeopardy" or "Double Jeopardy" card
                #  covering the category unless the game is being edited then the category name should show
                # this means the games should be opened in ProgramMode.Neutral and it calls for another
                # DisplayState
                self.category_displays[col].display_state = DisplayState.Category
                row = 0
                for item in category.items:
                    if segment == Segment.Jeopardy:
                        self.clue_displays[col][row].amount = self.base_amount + self.base_amount * row
                    elif segment == Segment.DoubleJeopardy:
                        self.clue_displays[col][row].amount = 2 * self.base_amount + 2 * self.base_amount * row
                    self.clue_displays[col][row].clue = item.clue
                    self.clue_displays[col][row].correct_response = item.response
                    self.clue_displays[col][row].display_state = DisplayState.Dollars
                    row += 1
                col += 1
        else:
            # fill the board for game.final_jeopardy[]
            pass

    def setCategoriesHidden(self, segment):
        """
        Covers the category names with a graphic depending on the segment, Jeopardy, Double Jeopardy or Final Jeopardy.
        :param: segment - ProgramSegment.Jeopardy, ProgramSegment.DoubleJeopardy or ProgramSegment.FinalJeopardy
        :return: None
        """
        for category_display in self.category_displays:
            category_display.hide_category = True
            if segment == Segment.Jeopardy:
                category_display.category_cover = QPixmap('../images/JeopardyCard.png')
            elif segment == Segment.DoubleJeopardy:
                category_display.category_cover = QPixmap('../images/JeopardyCard.png')
            else:
                category_display.category_cover = QPixmap('../images/JeopardyCard.png')

    def revealCategories(self):
        """
        Reveals the categories (if hidden) by changing DisplayUnit.hide_category to False on all of the category units
        :return:
        """
        for category_display in self.category_displays:
            category_display.hide_category = False

    def revealCategory(self, number):
        """
        Reveals the category represented by number
        :param number: an integer 0 through 5
        :return: None
        """
        self.category_displays[number].hide_category = False