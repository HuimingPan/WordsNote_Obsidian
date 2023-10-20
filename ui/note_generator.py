# Create the logic of ui
#
from PyQt5 import QtWidgets
from ui.interface import Ui_MainWindow
import win32clipboard
import win32con
import markdown
import get_data
import datetime, json, os
import re
class Note_Generator(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Note_Generator, self).__init__()
        self.setupUi(self)
        self.pushButton_start.clicked.connect(self.start)

    def start(self):
        print("start")
        input_mode = self.comboBox_inputmode.currentText()
        output_mode = self.comboBox_output_mode.currentText()

        if input_mode == "剪切板":
            input_text = read_from_clipboard()
        elif input_mode == "文本框":
            input_text = self.textEdit_input.toPlainText()
        elif input_mode == "文件":
            input_text = read_from_file()
        else:
            raise ValueError("输入模式错误")

        word_list = text_to_list(input_text)
        note_text = ""
        for word in word_list:
            try:
                word_obj = get_data.Word(word)
            except:
                continue
            note_text+= markdown.word_markdown(word_obj)

        if output_mode == "剪切板":
            self.output(note_text, "ClipBoard")
        elif output_mode == "文本框":
            self.output(note_text, "TextEdit")
        elif output_mode == "文件":
            self.output(note_text, "File")
        else:
            raise ValueError("输出模式错误")

    def output(self, text, mode):
        if mode == "ClipBoard":
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
        elif mode == "TextEdit":
            self.textEdit_output.setText(text)
        elif mode == "File":
            date = datetime.date.today().strftime("%Y-%m-%d")
            with open('info.json') as json_file:
                dir_info = json.load(json_file)
                obsidian_dir = dir_info["obsidian_dir"]
                file_dir = dir_info["English_dir"]
            filename = f"draft English {date}.md"
            path = os.path.join(obsidian_dir, file_dir, filename)
            with open(path, encoding="utf-8", mode="w+") as f:
                f.write(text)
        else:
            raise ValueError("输出模式错误")

def read_from_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

def text_to_list(text,sepereator=","):
    reg = r'([a-z]+)'
    reg = re.compile(reg)
    words = re.findall(reg, text)
    return words

def read_from_file():
    pass