from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import *
import jeopardy_ui
from models import *
from graphic_objects import *

class Jeopardy(QMainWindow, jeopardy_ui.JeopardyUI):

    def __init__(self, app, parent=None):
        super(Jeopardy, self).__init__(parent)
        self.app = app
        self.screen_geometry = self.getScreenGeometry()
        self.createUI()
        self.createBoard(self.screen_geometry, self.stage_set)
        self.game_loaded = False

        # class variables (is class variables the correct name?)
        self.game = Game()
        self.game_pathname = ""
        self.game_modified = False

        self.setProgramMode(ProgramMode.Empty)
        self.game_segment = Segment.Jeopardy

        self.base_amount = 200                  # the smallest number of dollars or points
                                                # by using this variable you can opt to change it later

    def getScreenGeometry(self):
        desktop = self.app.desktop()
        screenNumber = desktop.screenNumber(self)  # gets the screen the form is on
        return desktop.availableGeometry(screenNumber)  # as a QRect

    def file_open(self):
        print("Got to file_open.")
        print("Opening temporary game file: 'temp_saved_game'")
        if self.game_modified:
            print("Write the code to ask if the user wants to save the current game before opening a new one.")
        self.game = self.game.read_game('temp_saved_game')
        self.game.playable = True
        print("The game is marked playable = ", self.game.playable)
        self.game_loaded = True
        self.setProgramMode(ProgramMode.Neutral)
        self.hideCategories(self.game_segment)
        self.fillBoard(self.game, Segment.Jeopardy)

    def file_create(self):
        print("Got to file_create.")
        self.game_loaded = True
        self.setProgramMode(ProgramMode.Editing)
        self.board.category_displays[3].display_state = DisplayState.Category

    def file_close(self):
        print("Got to file_close.")
        # check for unsaved changes here
        self.game = Game()                      # clear out all the former game entries
        self.game_loaded = False
        self.setProgramMode(ProgramMode.Neutral)

    def file_save(self):
        print("Got to file_save.")

    def file_save_as(self):
        print("Got to file_save_as.")

    def file_print(self):
        print("Got to file_print")

    def file_exit(self):
        print("Got to file_exit.")
        self.close()

    def closeEvent(self, event):
        print("Got to closeEvent.", event)
        # check for unsaved files here

    def edit_modify_info(self):
        print("Got to edit_modify.")
        self.setProgramMode(ProgramMode.Editing)

    def edit_modify_jeopardy(self):
        print("Got to edit_modify_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.Jeopardy)
        self.revealCategories()

    def edit_modify_double_jeopardy(self):
        print("Got to edit_modify_double_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.DoubleJeopardy)
        self.revealCategories()

    def edit_modify_final_jeopardy(self):
        print("Got to edit_modify_final_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.FinalJeopardy)
        self.revealCategories()

    def edit_cut(self):
        print("Got to edit_cut.")

    def edit_copy(self):
        print("Got to edit_copy.")

    def edit_paste(self):
        print("Got to edit_paste.")

    def game_names(self):
        print("Got to game_names.")
        self.clue_displays[2][1].display_state = DisplayState.Clue

    def game_practice(self):
        print("Got to game_practice.")

    def game_play_jeopardy(self):
        print("Got to game_play_jeopardy.")
        self.setProgramMode(ProgramMode.Playing)
        self.setSegment(Segment.Jeopardy)
        self.hideCategories(Segment.Jeopardy)

    def game_play_double_jeopardy(self):
        print("Got to game_play_double_jeopardy")
        self.setProgramMode(ProgramMode.Playing)
        self.setSegment(Segment.DoubleJeopardy)
        self.hideCategories(Segment.DoubleJeopardy)

    def game_play_final_jeopardy(self):
        print("Got to game_play_final_jeoardy")
        self.setProgramMode(ProgramMode.Playing)
        self.setSegment(Segment.FinalJeopardy)
        self.hideCategories(Segment.FinalJeopardy)

    def game_correct(self):
        print("Got to game_correct.")

    def game_end(self):
        """
        Ends the current game and places the program in Neutral mode
        :return: None
        """
        print("Got to game_end")
        # :todo: First there should be a warning message before ending the game
        self.setProgramMode(ProgramMode.Neutral)


    def game_settings(self):
        print("Got to game_settings.")

        import time
        time.sleep(5)
        print("That was a quick sleep!")


    def help_using_program(self):
        print("Got to help_using_program.")

    def help_rules(self):
        print("Got to help_rules.")

    def help_about(self):
        print("Got to help_about.")

    def setProgramMode(self, mode):
        self.program_mode = mode
        if mode == ProgramMode.Empty:
            self.file_open_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(False)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(False)
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
            self.file_open_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(True)
            self.file_save_as_action.setEnabled(True)
            self.file_print_action.setEnabled(True)
            self.edit_modifyMenu.setEnabled(True)
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
            self.file_open_action.setEnabled(True)
            self.file_create_action.setEnabled(True)
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(True)
            self.file_save_as_action.setEnabled(True)
            self.file_print_action.setEnabled(True)
            self.edit_modifyMenu.setEnabled(True)
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
            self.file_open_action.setEnabled(False)
            self.file_create_action.setEnabled(False)
            self.file_close_action.setEnabled(False)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(False)
            self.edit_modifyMenu.setEnabled(False)
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
        display_unit_width = screen_geometry.width() * 0.1  # calculates 10% of the available height
        display_unit_height = display_unit_width * 9/16       # maintain a 16:9 aspect ratio
        display_unit_size = QSizeF(display_unit_width, display_unit_height)


        # calculate the gap between display units (5% of the width of the unit)
        gap = display_unit_size.width()/20

        # Create the category displays
        self.category_displays = []
        for col in range(6):
            element = DisplayUnit(display_unit_size, type=DisplayType.Category)
            element.setPos(col * (display_unit_size.width() + gap), 0)
            element.display_state = DisplayState.Blank
            self.category_displays.append(element)
            scene.addItem(element)

        # Create the clue displays
        self.clue_displays = []
        for col in range(6):
            row_list = []
            for row in range(5):
                element = DisplayUnit(display_unit_size, DisplayType.Clue)
                element.setPos(col * (display_unit_size.width() + gap),
                               display_unit_size.height() + 2 * gap + row * (display_unit_size.height() + gap))
                element.display_state = DisplayState.Blank
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


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('Jeopardy')
    form = Jeopardy(app)
    form.show()
    app.exec()
