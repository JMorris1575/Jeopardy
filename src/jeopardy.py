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

        # define the fonts to be used for the various types of display
        self.font_database = QFontDatabase()
        self.category_font_id = self.font_database.addApplicationFont("../fonts/Oswald-Bold.ttf")
        if self.category_font_id != -1:
            self.category_font = QFont("Oswald", 16)
            self.number_font = QFont("Oswald", 32)
        else:
            self.category_font = QFont("Arial", 16)
            self.number_font = QFont("Arial", 32, QFont.Bold)
        self.clue_font_id = self.font_database.addApplicationFont("../fonts/FjallaOne-Regular.ttf")
        if self.clue_font_id != -1:
            self.clue_font = QFont("Fjalla One", 12)
        else:
            self.clue_font = QFont("Times New Roman", 12)
        self.number_font = QFont("Arial", 32, QFont.Bold)

        self.base_amount = 200                  # the smallest number of dollars or points
                                                # by using this variable you can opt to change it later

        self.gamefile_changed = True            # temporarily initialized to True while building checkForSave feature
        self.game_filename = ""

        # compute the size of the DisplayUnits
        display_unit_width = self.screen_geometry.width() * 0.1  # calculates 10% of the available width
        display_unit_height = display_unit_width * 9/16       # maintain a 16:9 aspect ratio
        display_unit_size = QSizeF(display_unit_width, display_unit_height)
        print("in Jeopardy.__init__: display_unit_size = ", display_unit_size)

        # calculate the gap between display units (5% of the width of the unit)
        gap = display_unit_size.width()/20

        self.createBoard(self.stage_set, display_unit_size, gap)
        # self.stage_set.setSceneRect(0, 0, 1000, 600)
        # self.view.fitInView(self.stage_set.itemsBoundingRect(), Qt.KeepAspectRatio)
        print("in Jeopardy.__init__: self.view.sceneRect() = ", self.view.sceneRect())

    ################################################################################
    #                                                                              #
    #                               Menu Action Handlers                           #
    #                                                                              #
    ################################################################################

    # File Menu---------------------------------------------------------------------

    def file_open(self):
        print("Opening temporary game file: '../Games/temp_game.jqz'")
        # Check to see if the file in memory needs saving
        if self.game_modified:
            result = self.checkForSave()
            if result == QMessageBox.Cancel:
                return
            elif result == QMessageBox.Save:
                self.file_save()
        # need a dialog here to select a file
        self.game_pathname = '../games/temp_game.jqz'
        self.game = self.game.read_game(self.game_pathname)
        self.fillBoard()
        self.game.playable = self.game.isPlayable()
        print("The temporary game has been marked playable = ", self.game.playable)
        self.setProgramMode(ProgramMode.Neutral)
        self.setSegment(Segment.Jeopardy)

        # self.hideCategories(self.game_segment)
        # self.fillBoard(self.game, Segment.Jeopardy)
        print('at the end of file_open: self.size() = ', self.size())

    def file_create(self):
        print("Got to file_create.")
        self.createGame()

    def file_close(self):
        print("Got to file_close.")
        # check for unsaved changes here
        self.game = Game()                      # clear out all the former game entries
        self.setProgramMode(ProgramMode.Empty)

    def file_save(self):
        print("Got to file_save.")
        if self.game_pathname == '':
            self.file_save_as()
            return
        self.game.write_game(self.game_pathname)
        self.game_modified = False

    def file_save_as(self):
        print("Got to file_save_as.")
        # Just for now save the game to Games/temp_game.jqz
        self.game_pathname = '../Games/temp_game.jqz'
        self.game.write_game(self.game_pathname)
        self.game_modified = False

    def file_print(self):
        print("Got to file_print")

    def file_exit(self):
        print("Got to file_exit.")
        self.close()

    def closeEvent(self, event):
        print("Got to closeEvent.", event)
        if self.game_modified:
            result = self.checkForSave()
            if result == QMessageBox.Cancel:
                return
            elif result == QMessageBox.Save:
                self.file_save()
        if self.category_font_id != -1:
            self.font_database.removeApplicationFont(self.category_font_id)
        if self.clue_font_id != -1:
            self.font_database.removeApplicationFont(self.clue_font_id)
        # check for unsaved files here

    # Edit Menu ----------------------------------------------------------------------------

    def edit_modify_info(self):
        print("Got to edit_modify.")
        self.setProgramMode(ProgramMode.Editing)
        self.getGameInfo()

    def edit_modify_jeopardy(self):
        print("Got to edit_modify_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.Jeopardy)

    def edit_modify_double_jeopardy(self):
        print("Got to edit_modify_double_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.DoubleJeopardy)

    def edit_modify_final_jeopardy(self):
        print("Got to edit_modify_final_jeopardy.")
        self.setProgramMode(ProgramMode.Editing)
        self.setSegment(Segment.FinalJeopardy)

    def edit_exit_editing(self):
        print("Got to edit_exit_editing.")
        self.setProgramMode(ProgramMode.Neutral)
        self.resetBoard()

    def edit_cut(self):
        print("Got to edit_cut.")

    def edit_copy(self):
        print("Got to edit_copy.")

    def edit_paste(self):
        print("Got to edit_paste.")

    # Game Menu -------------------------------------------------------------------------

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

    # Help Menu -------------------------------------------------------------------------

    def help_using_program(self):
        print("Got to help_using_program.")

    def help_rules(self):
        print("Got to help_rules.")

    def help_about(self):
        print("Got to help_about.")

    ###############################################################################################
    #                                                                                             #
    #                                       Support Functions                                     #
    #                                                                                             #
    ###############################################################################################

    def checkForSave(self):
        """
        Checks if the user wants to save the current game file and, if so, saves it
        :return: QMessageBox response - either Save, Discard or Cancel
        """
        title = "Check For Save"
        message = "The current game file has been modified, do you want to save it?"
        buttons = QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        icon = QMessageBox.Question
        msgBox = QMessageBox(icon, title, message, buttons, self)
        msgBox.setDefaultButton(QMessageBox.Save)
        result = msgBox.exec()
        return result

    def getScreenGeometry(self):
        desktop = self.app.desktop()
        screenNumber = desktop.screenNumber(self)  # gets the screen the form is on
        return desktop.availableGeometry(screenNumber)  # as a QRect

    ###############################################################################################
    #                                                                                             #
    #                                      Main Functions                                         #
    #                                                                                             #
    ###############################################################################################

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
        self.resetBoard()

    def createBoard(self, scene, size, gap):
        """
        Creates a blank Jeopardy board for later use
        :param size: QFSize telling the width and height of the display units for this screen
        :return: None
        """

        # Create the category displays
        self.category_displays = []
        for col in range(6):
            element = DisplayUnit(size, DisplayType.Category, self, col, 0)
            element.setPos(col * (size.width() + gap), 0)
            element.setDisplayState(DisplayState.Blank)
            self.category_displays.append(element)
            scene.addItem(element)

        # Create the clue displays
        self.clue_displays = []
        for col in range(6):
            row_list = []
            for row in range(5):
                element = DisplayUnit(size, DisplayType.Clue, self, col, row+1)
                element.setPos(col * (size.width() + gap),
                               size.height() + 2 * gap + row * (size.height() + gap))
                if col == 0:
                    print('in createBoard: element.pos(), element.size() = ', element.pos(), element.size)
                element.setDisplayState(DisplayState.Blank)
                scene.addItem(element)
                row_list.append(element)
            self.clue_displays.append(row_list)

    def resetBoard(self):
        """
        Updates the board according to the current values of self.program_mode and self.game_segment
        :return: None
        """
        # first deal with each category
        for col in range(6):
            unit = self.category_displays[col]
            unit.setCoverCard(self.game_segment)
            if self.program_mode == ProgramMode.Neutral:
                unit.setDisplayState(DisplayState.SegmentCard)
            elif self.program_mode == ProgramMode.Empty:
                unit.setDisplayState(DisplayState.Blank)
            elif self.program_mode == ProgramMode.Editing:
                if self.game.board[col][0].isFilled(self.game_segment):
                    unit.setDisplayState(DisplayState.A_Text)
                else:
                    unit.setDisplayState(DisplayState.SegmentCard)
            elif self.program_mode == ProgramMode.Playing:
                unit.setDisplayState(DisplayState.SegmentCard)
            # now get all that category's clues
            for row in range(5):
                unit = self.clue_displays[col][row]
                unit.setCoverCard(self.game_segment)
                if self.program_mode == ProgramMode.Neutral:
                    unit.setDisplayState(DisplayState.Dollars)
                elif self.program_mode == ProgramMode.Empty:
                    unit.setDisplayState(DisplayState.Blank)
                elif self.program_mode == ProgramMode.Editing:
                    if self.game.board[col][row+1].isFilled(self.game_segment):
                        unit.setDisplayState(DisplayState.A_Text)
                    else:
                        unit.setDisplayState(DisplayState.SegmentCard)
                elif self.program_mode == ProgramMode.Playing:
                    unit.setDisplayState(DisplayState.Dollars)

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
        self.coverDisplays()
        self.setProgramMode(ProgramMode.Editing)
        # build the empty game
        self.game = Game("<name>", "<topic>", "<target group>")

    def getGameInfo(self):
        """
        Called from Edit->Modify->Game Info... to get information about the game to be used in the open dialog
        :return: None
        """
        game_info_dialog = GameInfoDialog(self.game.name, self.game.topic, self.game.target_group)
        if game_info_dialog.exec():
            self.game.name = game_info_dialog.name
            self.game.topic = game_info_dialog.topic
            groups = []
            for item in game_info_dialog.group:
                groups.append(item)
            self.game.target_group = groups

        self.game_modified = True

    def coverDisplays(self):
        """
        Covers all of the displays on the board by setting each unit's DisplayState to DisplayState.SegmentCard
        :return: None
        """
        for col in range(6):
            self.category_displays[col].setDisplayState(DisplayState.SegmentCard)
            for row in range(5):
                self.clue_displays[col][row].setDisplayState(DisplayState.SegmentCard)

    def fillBoard(self):
        """
        Fills all of the Category and Clue units with the text contents of every segment of the game
        :param game: and instance of the Game() class from which the information is drawn
        :return: None
        """
        for segment in Segment:
            if segment == Segment.FinalJeopardy:
                pass
            else:
                segment_name = segment.name
                for col in range(6):
                    unit = self.category_displays[col]
                    game_element = self.game.board[col][0]
                    if segment_name in game_element.text_A.keys():
                        text_A = game_element.text_A[segment_name]
                    else:
                        text_A = ''
                    if segment_name in game_element.text_B.keys():
                        text_B = game_element.text_B[segment_name]
                    else:
                        text_B = ''
                    unit.setContents(segment, text_A, text_B)
                    for row in range(5):
                        unit = self.clue_displays[col][row]
                        game_element = self.game.board[col][row+1]
                        if segment_name in game_element.text_A.keys():
                            text_A = game_element.text_A[segment_name]
                        else:
                            text_A = ''
                        if segment_name in game_element.text_B.keys():
                            text_B = game_element.text_B[segment_name]
                        else:
                            text_B = ''
                        unit.setContents(segment, text_A, text_B)
                        if segment_name == 'Jeopardy':
                            unit.contents[segment_name]['amount'] = self.base_amount + self.base_amount * row
                        elif segment_name == 'DoubleJeopardy':
                            unit.contents[segment_name]['amount'] = 2 * self.base_amount + 2 * self.base_amount * row

    def mousePressProcessing(self, unit, button):
        """
        Processes mouse events received from the DisplayUnits
        :param unit: the display unit that received the mouse press
        :param button: which button was pressed: Qt.LeftButton, Qt.RightButton or Qt.MiddleButton
        :return: None
        """
        if self.program_mode == ProgramMode.Editing:
            self.editGameElement(unit, button)
        elif self.program_mode == ProgramMode.Playing:
            unit.displayed_text = "Ready to reveal a clue."
        elif self.program_mode == ProgramMode.Neutral:
            unit.displayed_text = "Shift to Edit mode"
        elif self.program_mode == ProgramMode.Empty:
            unit.displayed_text = "Please load or create a game."
        else:
            unit.displayed_text = "Unknown program_mode in mousePressProcessing"

    def editGameElement(self, unit, button):
        """
        LeftClick allows the user to edit the contents of the Game() element displayed by the current unit
        RightClick toggles the displayed_text between the A_Text and the B_Text
        :param unit: The DisplayUnit that was clicked
        :return: None
        """
        if button == Qt.LeftButton:
            text_A = unit.contents[self.game_segment.name]['A']
            text_B = unit.contents[self.game_segment.name]['B']
            edit_dialog = ElementEditDialog(unit.type, text_A, text_B)
            if edit_dialog.exec():
                text_A = edit_dialog.text_A
                text_B = edit_dialog.text_B
                unit.setContents(self.game_segment, text_A, text_B)
                self.game.board[unit.col][unit.row].setContents(self.game_segment, text_A, text_B)
                if self.game.isPlayable():
                    self.game.playable = True
                unit.setDisplayState(DisplayState.A_Text)
                self.game_modified = True
        elif button == Qt.RightButton:
            if unit.display_state == DisplayState.A_Text:
                unit.setDisplayState(DisplayState.B_Text)
            elif unit.display_state == DisplayState.B_Text:
                unit.setDisplayState(DisplayState.A_Text)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('Jeopardy')
    form = Jeopardy(app)
    form.show()
    app.exec()
