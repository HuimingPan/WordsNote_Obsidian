"""
In this file, we define the main window, logic and functions of the user interface.
"""
import datetime
import json
import os
import re

import win32clipboard
import win32con
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from utilities import get_data, markdown
from .interface import Ui_MainWindow


class Note_Generator(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Note_Generator, self).__init__()
        self.setupUi(self)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_file.clicked.connect(self.open_file)

        self.radioButton_file.setChecked(True)
        self.textEdit_input.clear()

        self.parameters = json.load(open('info.json'))

    def start(self):
        input_text = self.textEdit_input.toPlainText()
        word_list = text_to_list(input_text)
        note_text = ""
        for word in word_list:
            try:
                word_obj = get_data.Word(word)
            except:
                continue
            note_text += markdown.word_markdown(word_obj)
        output_mode = "file" if self.radioButton_file.isChecked() else "clipboard"
        self.output(note_text, output_mode)

    def output(self, text, mode):
        if mode == "clipboard":
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
        elif mode == "file":
            date = datetime.date.today().strftime("%Y-%m-%d")
            filename = f"draft English {date}.md"
            path = os.path.join(self.parameters["obsidian_dir"],
                                self.parameters["English_dir"],
                                filename)
            with open(path, encoding="utf-8", mode="w+") as f:
                f.write(text)
        else:
            raise ValueError("输出模式错误")
        self.textEdit_input.append("已输出到" + mode)

    def open_file(self):
        try:
            file_path = os.path.join(self.parameters["Input_file_dir"], self.parameters["Input_file_name"])
            with open(file_path, encoding="utf-8") as f:
                text = f.read()
            self.textEdit_input.setText(text)
        except FileNotFoundError:
            file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件",
                                                               self.parameters["Input_file_dir"],
                                                               "Text Files (*.txt)")
            with open(file_name, encoding="utf-8") as f:
                text = f.read()
            self.textEdit_input.setText(text)
        if self.parameters["Auto_start"]:
            self.start()


def text_to_list(text, sepereator=","):
    reg = r'([a-z]+)'
    reg = re.compile(reg)
    words = re.findall(reg, text)
    return words
