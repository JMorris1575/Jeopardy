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
        self.setProgramState(ProgramState.Neutral)

        # class variables (is class variables the correct name?)
        self.game = Game()
        self.game_pathname = ""
        #:todo: figure out how to draw the board here - maybe see what was done in CardTablePractice - self.drawBoard(self.game)
        # self.updateBoard()
        # self.view.setScene((self.scene))

    # def updateBoard(self):
    #     item_list = self.scene.items()
    #     print(len(item_list))
    #     for item in item_list:
    #         print(item)

    def getScreenGeometry(self):
        desktop = self.app.desktop()
        screenNumber = desktop.screenNumber(self)  # gets the screen the form is on
        return desktop.availableGeometry(screenNumber)  # as a QRect

    def file_open(self):
        print("Got to file_open.")
        print("Opening temporary game file: 'temp_saved_game'")
        self.game.read_game('temp_saved_game')  # this doesn't keep the opened game - needs to say something = self.game.read_game(<filename>)
        self.game.playable = True
        print("The game is marked playable = ", self.game.playable)
        self.setProgramState(ProgramState.Editing)

    def file_create(self):
        print("Got to file_create.")
        self.setProgramState(ProgramState.Editing)
        self.board.category_displays[3].display_state = DisplayState.Category

    def file_close(self):
        print("Got to file_close.")
        self.setProgramState(ProgramState.Neutral)

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

    def edit_modify(self):
        print("Got to edit_modify_info.")

    def edit_cut(self):
        print("Got to edit_cut.")

    def edit_copy(self):
        print("Got to edit_copy.")

    def edit_paste(self):
        print("Got to edit_paste.")

    def game_names(self):
        print("Got to game_names.")
        self.board.clue_displays[2][1].display_state = DisplayState.Clue
        self.board.clue_displays[2][1].clue = "Once upon a time"
        print()

    def game_practice(self):
        print("Got to game_practice.")

    def game_play(self):
        print("Got to game_play.")
        self.setProgramState(ProgramState.Playing)

    def game_correct(self):
        print("Got to game_correct.")

    def help_using_program(self):
        print("Got to help_using_program.")

    def help_rules(self):
        print("Got to help_rules.")

    def help_about(self):
        print("Got to help_about.")

    def setProgramState(self, state):
        self.programState = state
        if state == ProgramState.Neutral:
            self.file_close_action.setEnabled(False)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(False)
            self.edit_modify_action.setEnabled(False)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            self.game_play_action.setEnabled(False)
            self.game_correct_action.setEnabled(False)
        elif state == ProgramState.Editing:
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(True)
            self.file_save_as_action.setEnabled(True)
            self.file_print_action.setEnabled(True)
            self.edit_modify_action.setEnabled(True)
            self.edit_cut_action.setEnabled(True)
            self.edit_copy_action.setEnabled(True)
            self.edit_paste_action.setEnabled(True)
            if self.game.playable:
                self.game_play_action.setEnabled(True)
                self.game_correct_action.setEnabled(True)
        elif state == ProgramState.Playing:
            self.file_close_action.setEnabled(True)
            self.file_save_action.setEnabled(False)
            self.file_save_as_action.setEnabled(False)
            self.file_print_action.setEnabled(True)
            self.edit_modify_action.setEnabled(True)
            self.edit_cut_action.setEnabled(False)
            self.edit_copy_action.setEnabled(False)
            self.edit_paste_action.setEnabled(False)
            if self.game.playable:
                self.game_play_action.setEnabled(True)
                self.game_correct_action.setEnabled(True)
        else:
            print("Set program state called with unrecognized state.")


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('Jeopardy')
    form = Jeopardy(app)
    form.show()
    app.exec()
