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

from utilities import get_data, markdown, repeatability
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


        # Check if the word has been recorded before.
        word_repeat_list = repeatability.check_word(word_list)
        if word_repeat_list:
            word_repeat_text = "以下单词已经记录过：\n"
            for word, date in word_repeat_list:
                word_repeat_text += f"{word}, {date}\n"
                word_list.remove(word)
            self.textEdit_input.append(word_repeat_text)

        # Append the word to the file with the date it was first recorded.

        word_wrong_list = []
        word_found_list = []
        for word in word_list:
            try:
                word_obj = get_data.Word(word)
                word_found_list.append(word)
            except:
                word_wrong_list.append(word)
                continue
            note_text += markdown.word_markdown(word_obj)
        if word_wrong_list:
            word_wrong_text = "以下单词未找到：\n"
            for word in word_wrong_list:
                word_wrong_text += f"{word}\n"
            self.textEdit_input.append(word_wrong_text)
        repeatability.append_word(word_found_list)
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
