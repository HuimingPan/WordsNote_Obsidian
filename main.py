from ui import Note_Generator
from PyQt5 import QtWidgets

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Note_Generator()
    ui.show()
    sys.exit(app.exec_())
