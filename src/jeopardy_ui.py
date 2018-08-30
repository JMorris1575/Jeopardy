from graphic_objects import *
from models import *

class Stage(QGraphicsView):

    def __init__(self, parent=None):
        super(Stage, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        print("Got to mousePressEvent in Stage class.")

class JeopardyUI(object):

    def createUI(self):

        ###########################################################################################
        #                                                                                         #
        #                                       menuBar                                           #
        #                                                                                         #
        ###########################################################################################

        # fileMenu --------------------------------------------------------------------------------

        fileMenu = self.menuBar().addMenu("&File")
        self.file_open_action = fileMenu.addAction("&Open...")
        self.file_open_action.setShortcuts(QKeySequence.Open)
        self.file_open_action.triggered.connect(self.file_open)

        self.file_create_action = fileMenu.addAction("&Create...")
        self.file_create_action.triggered.connect(self.file_create)

        self.file_close_action = fileMenu.addAction("Close Game")
        self.file_close_action.setShortcuts(QKeySequence.Close)
        self.file_close_action.triggered.connect(self.file_close)

        fileMenu.addSeparator()

        self.file_save_action = fileMenu.addAction("&Save")
        self.file_save_action.setShortcuts(QKeySequence.Save)
        self.file_save_action.triggered.connect(self.file_save)

        self.file_save_as_action = fileMenu.addAction("Save &As...")
        self.file_save_as_action.setShortcuts(QKeySequence.SaveAs)
        self.file_save_as_action.triggered.connect(self.file_save_as)

        fileMenu.addSeparator()

        self.file_print_action = fileMenu.addAction("&Print Leader Notes...")
        self.file_print_action.setShortcuts(QKeySequence.Print)
        self.file_print_action.triggered.connect(self.file_print)

        fileMenu.addSeparator()

        self.file_exit_action = fileMenu.addAction("E&xit")
        self.file_exit_action.triggered.connect(self.file_exit)

        # editMenu --------------------------------------------------------------------------------

        editMenu = self.menuBar().addMenu("&Edit")

        self.edit_modifyMenu = editMenu.addMenu("&Modify")
        self.edit_modify_info_action = self.edit_modifyMenu.addAction("&Game Information")
        self.edit_modify_info_action.setToolTip("Add or edit background information for this game.")
        self.edit_modify_info_action.triggered.connect(self.edit_modify_info)
        self.edit_modify_jeopardy_action = self.edit_modifyMenu.addAction("&Jeopardy")
        self.edit_modify_jeopardy_action.setToolTip("Edit Items for the Jeopardy Segment")
        self.edit_modify_jeopardy_action.triggered.connect(self.edit_modify_jeopardy)
        self.edit_modify_double_jeopardy_action = self.edit_modifyMenu.addAction("&Double Jeopardy")
        self.edit_modify_double_jeopardy_action.setToolTip("Edit Items for the Double Jeopardy Segment")
        self.edit_modify_double_jeopardy_action.triggered.connect(self.edit_modify_double_jeopardy)
        self.edit_modify_final_jeopardy_action = self.edit_modifyMenu.addAction("&Final Jeopardy")
        self.edit_modify_final_jeopardy_action.setToolTip("Edit Items for the Final Jeopardy Segment")
        self.edit_modify_final_jeopardy_action.triggered.connect(self.edit_modify_final_jeopardy)
        self.edit_exit_editing_action = editMenu.addAction("E&xit Editing")
        self.edit_exit_editing_action.triggered.connect(self.edit_exit_editing)

        editMenu.addSeparator()

        self.edit_cut_action = editMenu.addAction("Cu&t")
        self.edit_cut_action.setShortcuts(QKeySequence.Cut)
        self.edit_cut_action.triggered.connect(self.edit_cut)

        self.edit_copy_action = editMenu.addAction("&Copy")
        self.edit_copy_action.setShortcuts(QKeySequence.Copy)
        self.edit_copy_action.triggered.connect(self.edit_copy)

        self.edit_paste_action = editMenu.addAction("&Paste")
        self.edit_paste_action.setShortcuts(QKeySequence.Paste)
        self.edit_paste_action.triggered.connect(self.edit_paste)

        # gameMenu --------------------------------------------------------------------------------

        gameMenu = self.menuBar().addMenu("&Game")

        self.game_names_action = gameMenu.addAction("Enter &Names")
        self.game_names_action.triggered.connect(self.game_names)

        self.game_practice_action = gameMenu.addAction("&Practice")
        self.game_practice_action.triggered.connect(self.game_practice)

        gameMenu.addSeparator()

        self.game_playMenu = gameMenu.addMenu("&Play")
        self.game_play_jeopardy_action = self.game_playMenu.addAction("&Jeopardy")
        self.game_play_jeopardy_action.triggered.connect(self.game_play_jeopardy)
        self.game_play_double_jeopardy_action = self.game_playMenu.addAction("&Double Jeopardy")
        self.game_play_double_jeopardy_action.triggered.connect(self.game_play_double_jeopardy)
        self.game_play_final_jeopardy_action = self.game_playMenu.addAction("&Final Jeopardy")
        self.game_play_final_jeopardy_action.triggered.connect(self.game_play_final_jeopardy)

        self.game_correct_action = gameMenu.addAction("&Correct Scoring Errors")
        self.game_correct_action.triggered.connect(self.game_correct)

        self.game_end_action = gameMenu.addAction("&End this Game")
        self.game_end_action.triggered.connect(self.game_end)

        gameMenu.addSeparator()

        self.game_settings_action = gameMenu.addAction("Settings...")
        self.game_settings_action.triggered.connect(self.game_settings)

        # helpMenu --------------------------------------------------------------------------------

        helpMenu = self.menuBar().addMenu("&Help")

        self.help_using_program_action = helpMenu.addAction("&Using the Program")
        self.help_using_program_action.triggered.connect(self.help_using_program)

        self.help_rules_action = helpMenu.addAction("&Rules of Jeopardy")
        self.help_rules_action.triggered.connect(self.help_rules)

        helpMenu.addSeparator()

        self.help_about_action = helpMenu.addAction("&About")
        self.help_about_action.triggered.connect(self.help_about)

        ###########################################################################################
        #                                                                                         #
        #                            Scene, Viewport and Central Widget                           #
        #                                                                                         #
        ###########################################################################################

        self.stage_set = QGraphicsScene()
        self.stage_set.setBackgroundBrush(Qt.black)

        self.view = QGraphicsView()
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.view.setScene(self.stage_set)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setCentralWidget(self.view)
