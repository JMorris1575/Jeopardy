from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphic_objects import *

class JeopardyUI(object):

    def getElementSize(self):
        desktop = self.app.desktop()
        screenNumber = desktop.screenNumber(self)  # gets the screen the form is on
        screenGeometry = desktop.availableGeometry(screenNumber)  # as a QRect
        element_width = screenGeometry.width() * 0.1  # calculates 10% of the available height
        element_height = element_width * 9/16       # maintain a 16:9 aspect ratio
        return QSizeF(element_width, element_height)

    def createUI(self, callerObject):

        ##########################################
        #                                        #
        #              menuBar                   #
        #                                        #
        ##########################################

        # fileMenu

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

        # editMenu

        editMenu = self.menuBar().addMenu("&Edit")

        self.edit_modify_action = editMenu.addAction("&Modify Game")
        self.edit_modify_action.triggered.connect(self.edit_modify)

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

        # gameMenu

        gameMenu = self.menuBar().addMenu("&Game")

        self.game_names_action = gameMenu.addAction("Enter &Names")
        self.game_names_action.triggered.connect(self.game_names)

        self.game_practice_action = gameMenu.addAction("&Practice")
        self.game_practice_action.triggered.connect(self.game_practice)

        self.game_play_action = gameMenu.addAction("Play &Jeopardy!")
        self.game_play_action.triggered.connect(self.game_play)

        self.game_correct_action = gameMenu.addAction("&Correct Scoring Errors")
        self.game_correct_action.triggered.connect(self.game_correct)

        # helpMenu

        helpMenu = self.menuBar().addMenu("&Help")

        self.help_using_program_action = helpMenu.addAction("&Using the Program")
        self.help_using_program_action.triggered.connect(self.help_using_program)

        self.help_rules_action = helpMenu.addAction("&Rules of Jeopardy")
        self.help_rules_action.triggered.connect(self.help_rules)

        helpMenu.addSeparator()

        self.help_about_action = helpMenu.addAction("&About")
        self.help_about_action.triggered.connect(self.help_about)

        # Central Widget

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.black)

        desktop = self.app.desktop()
        size = self.getElementSize()
        gap = size.width()/20

        self.category_displays = []
        for col in range(6):
            element = BoardScreen(size)
            element.setPos(col * (size.width() + gap), 0)
            self.category_displays.append(element)
            self.scene.addItem(element)
        self.clue_displays = [[]]
        for col in range(6):
            for row in range(5):
                row_list = []
                element = BoardScreen(size)
                element.setPos(col * (size.width() + gap), size.height() + 2 * gap + row * (size.height() + gap))
                self.scene.addItem(element)
                row_list.append(element)
            self.clue_displays.append(row_list)

        self.view = QGraphicsView()
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate) #todo: find out what this does

        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

