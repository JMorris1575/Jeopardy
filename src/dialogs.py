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

        layout_A = QHBoxLayout()
        layout_A.addWidget(label_A)
        layout_A.addWidget(self.line_edit_A)

        layout_B = QHBoxLayout()
        layout_B.addWidget(label_B)
        layout_B.addWidget(self.line_edit_B)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.acceptEdit)
        button_box.rejected.connect(self.cancelEdit)

        layout = QVBoxLayout()
        layout.addLayout(layout_A)
        layout.addLayout(layout_B)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def acceptEdit(self):
        self.text_A = self.line_edit_A.text()
        self.text_B = self.line_edit_B.text()
        self.accept()

    def cancelEdit(self):
        print("Got to dialogs.py cancelEdit.")
        self.reject()