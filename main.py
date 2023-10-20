from ui.note_generator import Note_Generator
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Note_Generator()
    ui.show()
    sys.exit(app.exec_())
