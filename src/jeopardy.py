from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import *
from dialogs import *

import jeopardy_ui
from models import *
from graphic_objects import *


class Jeopardy(QMainWindow, jeopardy_ui.JeopardyUI):

    def __init__(self, app, parent=None):
        super(Jeopardy, self).__init__(parent)
        self.app = app
        self.screen_geometry = self.getScreenGeometry()
        self.createUI()
        self.game_loaded = False

        # class variables (is class variables the correct name?)
        self.game = Game()
        self.game_pathname = ""
        self.game_modified = False

        self.setProgramMode(ProgramMode.Empty)
        self.game_segment = Segment.Jeopardy

        self.category_font = QFont("Arial", 16)
        self.font_database = QFontDatabase()
        self.clue_font_id = self.font_database.addApplicationFont("../fonts/GenBkBasBI.ttf")
        if self.clue_font_id != -1:
            self.clue_font = QFont("Gentium Book Basic", 12)
        else:
            self.clue_font = QFont("Times New Roman", 18)
        self.number_font = QFont("Arial", 32, QFont.Bold)

        self.base_amount = 200                  # the smallest number of dollars or points
                                                # by using this variable you can opt to change it later

        self.gamefile_changed = True            # temporarily initialized to True while building checkForSave feature
        self.game_filename = ""

        self.createBoard(self.screen_geometry, self.stage_set)

    def getScreenGeometry(self):
        desktop = self.app.desktop()
        screenNumber = desktop.screenNumber(self)  # gets the screen the form is on
        return desktop.availableGeometry(screenNumber)  # as a QRect

    def setProgramMode(self, mode):
        self.program_mode = mode
        if mode == ProgramMode.Empty:
            self.stage_set.setBackgroundBrush(QColor(Qt.black))
            self.file_open_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(False)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(False)
            self.edit_exit_editing_action.setEnabled(False)
            self.edit_modifyMenu.setEnabled(False)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            self.game_names_action.setEnabled(True)
            self.game_practice_action.setEnabled(True)
            self.game_playMenu.setEnabled(False)
            self.game_correct_action.setEnabled(False)
            self.game_end_action.setEnabled(False)
        elif mode == ProgramMode.Neutral:
            self.stage_set.setBackgroundBrush(QColor(Qt.black))
            self.file_open_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(True)
            self.file_save_as_action.setEnabled(True)
            self.file_print_action.setEnabled(True)
            self.edit_modifyMenu.setEnabled(True)
            self.edit_exit_editing_action.setEnabled(False)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            self.game_names_action.setEnabled(True)
            self.game_practice_action.setEnabled(True)
            if self.game.playable:
                self.game_playMenu.setEnabled(True)
            else:
                self.game_playMenu.setEnabled(False)
            self.game_correct_action.setEnabled(False)
            self.game_end_action.setEnabled(False)
        elif mode == ProgramMode.Editing:
            self.stage_set.setBackgroundBrush(QColor(Qt.darkGray))
            self.file_open_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(True)
            self.file_save_as_action.setEnabled(True)
            self.file_print_action.setEnabled(True)
            self.edit_modifyMenu.setEnabled(True)
            self.edit_exit_editing_action.setEnabled(True)
            self.edit_cut_action.setEnabled(True)
            self.edit_copy_action.setEnabled(True)
            # the availability of the paste option should depend on whether there is anything on the clipboard
            self.edit_paste_action.setEnabled(True)
            self.game_names_action.setEnabled(False)
            self.game_practice_action.setEnabled(False)
            self.game_playMenu.setEnabled(False)
            self.game_correct_action.setEnabled(False)
            self.game_end_action.setEnabled(False)
        elif mode == ProgramMode.Playing:
            self.stage_set.setBackgroundBrush(QColor(Qt.black))
            self.file_open_action.setEnabled(False)
            self.file_create_action.setEnabled(False)
            self.file_close_action.setEnabled(False)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(False)
            self.edit_modifyMenu.setEnabled(False)
            self.edit_exit_editing_action.setEnabled(False)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            self.game_names_action.setEnabled(True)
            self.game_practice_action.setEnabled(True)
            self.game_playMenu.setEnabled(True)
            self.game_correct_action.setEnabled(True)
            self.game_end_action.setEnabled(True)
        else:
            print("setProgramMode called with unrecognized mode.")

    def getProgramMode(self):
        return self.program_mode

    def setSegment(self, segment):
        """
        Sets self.game_segment to the current segment and updates the board accordingly
        :param segment: and element of the Segment Enum
        :return: None
        """
        self.game_segment = segment
        self.fillBoard(self.game, segment)

    def createBoard(self, screen_geometry, scene):
        """
        Creates a blank Jeopardy board for later use
        :param size: QFSize telling the width and height of the display units for this screen
        :return: None
        """
        # compute the size of the DisplayUnits
        display_unit_width = screen_geometry.width() * 0.1  # calculates 10% of the available width
        display_unit_height = display_unit_width * 9/16       # maintain a 16:9 aspect ratio
        display_unit_size = QSizeF(display_unit_width, display_unit_height)


        # calculate the gap between display units (5% of the width of the unit)
        gap = display_unit_size.width()/20

        # Create the category displays
        self.category_displays = []
        for col in range(6):
            element = DisplayUnit(display_unit_size, DisplayType.Category, self, col)
            element.setPos(col * (display_unit_size.width() + gap), 0)
            element.setDisplayState(DisplayState.Blank)
            self.category_displays.append(element)
            scene.addItem(element)

        # Create the clue displays
        self.clue_displays = []
        for col in range(6):
            row_list = []
            for row in range(5):
                element = DisplayUnit(display_unit_size, DisplayType.Clue, self, col, row)
                element.setPos(col * (display_unit_size.width() + gap),
                               display_unit_size.height() + 2 * gap + row * (display_unit_size.height() + gap))
                element.setDisplayState(DisplayState.Blank)
                scene.addItem(element)
                row_list.append(element)
            self.clue_displays.append(row_list)

    def hideCategories(self, segment):
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
                category_display.category_cover = QPixmap('../images/DoubleJeopardyCard.png')
            else:
                category_display.category_cover = QPixmap('../images/FinalJeopardyCard.png')

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

    def createGame(self):
        """
        Called from File->Create... to create a new game
        :return: None
        """
        # Check to see if the file in memory needs saving
        if self.game_modified:
            result = self.checkForSave()
            if result == QMessageBox.Cancel:
                return
        self.setProgramMode(ProgramMode.Editing)
        # build the empty game
        self.game = Game("<name>", "<topic>", "<target group>")
        for segment in Segment:
            if segment.name != 'FinalJeopardy':
                for i in range(6):
                    category = Category("", "")
                    for j in range(5):
                        item = Item('', '')
                        category.add_item(item)
                    self.game.add_category(segment, category)
            else:
                category = Category('Final Jeopardy Category', 'Final Jeopardy Category Explanation')
                item = Item('Final Jeopardy Clue', 'Final Jeopardy Response')
                category.add_item(item)
                self.game.add_category(segment, category)
        # set the clue displays to DisplayState.Text_A
        for col in range(6):
            for row in range(5):
                self.clue_displays[col][row].setDisplayState(DisplayState.A_Text)
        # display the newly created game on the screen
        self.fillBoard(self.game, Segment.Jeopardy)

    def fillBoard(self, game, segment):
        """
        Fills all of the Category and Clue units -- currently also sets the display state better set elsewhere
        :param game: an instance of the Game class
        :param segment: a member of the Segment class: Segment.Jeopardy, Segment.DoubleJeopardy or Segment.FinalJeopardy
        :return: None
        """
        if segment == Segment.Jeopardy or segment == Segment.DoubleJeopardy:
            categories = game.get_categories(segment)
            col = 0
            for category in categories:
                self.category_displays[col].text_A = category.title
                self.category_displays[col].text_B = category.explanation
                # the following line is temporary. Later it should display a "Jeopardy" or "Double Jeopardy" card
                #  covering the category unless the game is being edited then the category name should show
                # this means the games should be opened in ProgramMode.Neutral and it calls for another
                # DisplayState
                # self.category_displays[col].setDisplayState(DisplayState.A_Text)
                row = 0
                for item in category.items:
                    if segment == Segment.Jeopardy:
                        self.clue_displays[col][row].amount = self.base_amount + self.base_amount * row
                    elif segment == Segment.DoubleJeopardy:
                        self.clue_displays[col][row].amount = 2 * self.base_amount + 2 * self.base_amount * row
                    self.clue_displays[col][row].text_A = item.clue
                    self.clue_displays[col][row].text_B = item.response
                    # self.clue_displays[col][row].setDisplayState(DisplayState.Dollars)
                    row += 1
                col += 1
        else:
            # fill the board for game.final_jeopardy[]
            pass

    def mousePressProcessing(self, unit, button):
        """
        Processes mouse events received from the DisplayUnits
        :param unit: the display unit that received the mouse press
        :param button: which button was pressed: Qt.LeftButton, Qt.RightButton or Qt.MiddleButton
        :return: None
        """
        if self.program_mode == ProgramMode.Editing:
            self.editGameElement(unit)
        elif self.program_mode == ProgramMode.Playing:
            unit.displayed_text = "Ready to reveal a clue."
        elif self.program_mode == ProgramMode.Neutral:
            unit.displayed_text = "Shift to Edit mode"
        elif self.program_mode == ProgramMode.Empty:
            unit.displayed_text = "Please load or create a game."
        else:
            unit.displayed_text = "Unknown program_mode in mousePressProcessing"

    def editGameElement(self, unit):
        """
        Allows the user to edit the contents of the Game() element displayed by the current unit
        :param unit: The DisplayUnit that was clicked
        :return: None
        """
        # unit.setDisplayState(DisplayState.A_Text)
        # unit._text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        edit_dialog = ElementEditDialog(unit.type, unit.text_A, unit.text_B)
        if edit_dialog.exec():
            text_A = edit_dialog.line_edit_A.text()
            text_B = edit_dialog.line_edit_B.text()
            unit.text_A = text_A
            unit.text_B = text_B
            if unit.type == DisplayType.Category:
                if self.game_segment == Segment.Jeopardy:
                    self.game.jeopardy[unit.col].title = text_A
                    self.game.jeopardy[unit.col].explanation = text_B
                elif self.game_segment == Segment.DoubleJeopardy:
                    self.game.double_jeopardy[unit.col].title = text_A
                    self.game.double_jeopardy[unit.col].explanation = text_B
                else:
                    self.game.final_jeopardy[unit.col].title = text_A
                    self.game.final_jeopardy[unit.col].explanation = text_B
            else:
                if self.game_segment == Segment.Jeopardy:
                    self.game.jeopardy[unit.col].items[unit.row].clue = text_A
                    self.game.jeopardy[unit.col].items[unit.row].response = text_B
                elif self.game_segment == Segment.DoubleJeopardy:
                    self.game.double_jeopardy[unit.col].items[unit.row].clue = text_A
                    self.game.double_jeopardy[unit.col].items[unit.row].response = text_B
                else:
                    self.game.final_jeopardy[unit.col].items[unit.row].clue = text_A
                    self.game.final_jeopardy[unit.col].items[unit.row].response = text_B
            unit.setDisplayState(DisplayState.A_Text)

            # you need to re-think how to get information from the Game() class to the DisplayUnits
            # it would be nice to have a fillUnit() method that takes the information from the edit_dialog box
            # and
            self.game_modified = True


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('Jeopardy')
    form = Jeopardy(app)
    form.show()
    app.exec()
