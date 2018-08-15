from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import *
import jeopardy_ui
from models import *

class Jeopardy(QMainWindow, jeopardy_ui.JeopardyUI):

    def __init__(self, app, parent=None):
        super(Jeopardy, self).__init__(parent)
        self.app = app
        self.screenGeometry = self.getScreenGeometry()
        self.createUI(self.screenGeometry)
        self.game_loaded = False

        # class variables (is class variables the correct name?)
        self.game = Game()
        self.game_pathname = ""
        self.game_modified = False

        self.setProgramMode(ProgramMode.Empty)
        self.game_segment = Segment.Jeopardy

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
        self.board.setCategoriesHidden(self.game_segment)
        self.board.fillBoard(self.game, Segment.Jeopardy)

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
        self.board.revealCategories()

    def edit_modify_double_jeopardy(self):
        print("Got to edit_modify_double_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.DoubleJeopardy)

    def edit_modify_final_jeopardy(self):
        print("Got to edit_modify_final_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.FinalJeopardy)

    def edit_cut(self):
        print("Got to edit_cut.")

    def edit_copy(self):
        print("Got to edit_copy.")

    def edit_paste(self):
        print("Got to edit_paste.")

    def game_names(self):
        print("Got to game_names.")
        self.board.clue_displays[2][1].display_state = DisplayState.Clue

    def game_practice(self):
        print("Got to game_practice.")

    def game_play_jeopardy(self):
        print("Got to game_play_jeopardy.")
        self.setProgramMode(ProgramMode.Playing)
        self.game_segment = Segment.Jeopardy

    def game_play_double_jeopardy(self):
        print("Got to game_play_double_jeopardy")
        self.setProgramMode(ProgramMode.Playing)
        self.game_segment = Segment.DoubleJeopardy

    def game_play_final_jeopardy(self):
        print("Got to game_play_final_jeoardy")
        self.setProgramMode(ProgramMode.Playing)
        self.game_segment = Segment.FinalJeopardy

    def game_correct(self):
        print("Got to game_correct.")

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
        if mode == ProgramMode.Neutral:
            self.file_close_action.setEnabled(False)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(False)
            if self.game_loaded:
                self.edit_modifyMenu.setEnabled(True)
            else:
                self.edit_modifyMenu.setEnabled(False)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            self.game_playMenu.setEnabled(False)
            self.game_correct_action.setEnabled(False)
        elif mode == ProgramMode.Editing:
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(True)
            self.file_save_as_action.setEnabled(True)
            self.file_print_action.setEnabled(True)
            self.edit_modifyMenu.setEnabled(True)
            self.edit_cut_action.setEnabled(True)
            self.edit_copy_action.setEnabled(True)
            self.edit_paste_action.setEnabled(True)
            if self.game.playable:
                self.game_playMenu.setEnabled(True)
                self.game_correct_action.setEnabled(True)
            else:
                self.game_playMenu.setEnabled(False)
                self.game_correct_action.setEnabled(False)
        elif mode == ProgramMode.Playing:
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(True)
            self.edit_modifyMenu.setEnabled(True)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            if self.game.playable:
                self.game_playMenu.setEnabled(True)
                self.game_correct_action.setEnabled(True)
            else:
                self.game_playMenu.setEnabled(False)
                self.game_correct_action.setEnabled(False)
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
        self.board.fillBoard(self.game, segment)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('Jeopardy')
    form = Jeopardy(app)
    form.show()
    app.exec()
