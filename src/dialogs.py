# A collection of Dialog boxes for the Jeopardy! program

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import *

class ElementEditDialog(QDialog):

    def __init__(self, type, text_A, text_B, parent=None):
        super(ElementEditDialog, self).__init__(parent)
        self.type = type
        self.text_A = text_A
        self.text_B = text_B

        self.setupUI()

    def setupUI(self):

        if self.type == DisplayType.Category:
            label_A = QLabel("Category Name:")
            label_B = QLabel("Category Explanation:")
        else:
            label_A = QLabel("Clue:")
            label_B = QLabel("Correct Response:")

        self.line_edit_A = QLineEdit()
        self.line_edit_A.setText(self.text_A)
        self.line_edit_B = QLineEdit()
        self.line_edit_B.setText(self.text_B)

        grid_layout = QGridLayout()
        grid_layout.addWidget(label_A, 0, 0)
        grid_layout.addWidget(self.line_edit_A, 0, 1)
        grid_layout.addWidget(label_B, 1, 0)
        grid_layout.addWidget(self.line_edit_B)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.acceptEdit)
        button_box.rejected.connect(self.cancelEdit)

        layout = QVBoxLayout()
        layout.addLayout(grid_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def acceptEdit(self):
        self.text_A = self.line_edit_A.text()
        self.text_B = self.line_edit_B.text()
        self.accept()

    def cancelEdit(self):
        print("Got to dialogs.py cancelEdit.")
        self.reject()


class GameInfoDialog(QDialog):

    def __init__(self, name, topic, group, parent=None):
        super(GameInfoDialog, self).__init__(parent)
        self.name = name
        self.topic = topic
        self.group = group
        self.setupUI()

    def setupUI(self):

        label_name = QLabel('Name:')
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.name)
        label_name.setBuddy(self.name_edit)
        self.name_edit.setToolTip('Give the game a name. It will be used to create a filename.')

        label_topic = QLabel('Topic:')
        self.topic_edit = QLineEdit()
        self.topic_edit.setText(self.topic)
        label_topic.setBuddy(self.topic_edit)
        self.topic_edit.setToolTip('If this game has a special theme or topic, enter it here.')

        label_group = QLabel('Target Group:')
        self.group_edit = QLineEdit()
        self.group_edit.setText(self.group)
        label_group.setBuddy(self.group_edit)
        self.group_edit.setToolTip('If this game is aimed at particular groups, list them here separated by commas.')

        grid_layout = QGridLayout()
        grid_layout.addWidget(label_name,0, 0)
        grid_layout.addWidget(self.name_edit, 0, 1)
        grid_layout.addWidget(label_topic, 1, 0)
        grid_layout.addWidget(self.topic_edit, 1, 1)
        grid_layout.addWidget(label_group, 2, 0)
        grid_layout.addWidget(self.group_edit, 2, 1)
        grid_layout.setColumnStretch(0, 3)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.acceptEdit)
        button_box.rejected.connect(self.cancelEdit)

        layout = QVBoxLayout()
        layout.addLayout(grid_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def acceptEdit(self):
        self.name = self.name_edit.text()
        self.topic = self.topic_edit.text()
        self.group = self.group_edit.text()
        self.accept()

    def cancelEdit(self):
        self.reject()

