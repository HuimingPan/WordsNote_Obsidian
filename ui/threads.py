from PyQt5.QtCore import QThread, pyqtSignal
from utilities import get_data, markdown, repeatability

class Web_handler(QThread):
    note_signal = pyqtSignal(str)
    def __init__(self, words:list, window):
        super(Web_handler, self).__init__()
        self.words = words
        self.window = window
    def run(self):
        # Check if the word has been recorded before.
        word_repeat_list = repeatability.check_word(self.words)

        if word_repeat_list:
            word_repeat_text = "以下单词已经记录过：\n"
            for word, date in word_repeat_list:
                word_repeat_text += f"{word}, {date}\n"
                self.words.remove(word)
            self.window.textEdit_input.append(word_repeat_text)

        note_text = ""
        word_wrong_list = []
        word_found_list = []
        for word in self.words:
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
            self.window.textEdit_input.append(word_wrong_text)
        repeatability.append_word(word_found_list)
        output_mode = "file" if self.window.radioButton_file.isChecked() else "clipboard"
        self.note_signal.emit(note_text)
