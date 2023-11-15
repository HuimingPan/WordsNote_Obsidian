import win32clipboard
import win32con
from utilities import get_data, markdown

"""
In this file, enter the word to be looked up in console and paste it into ClipBoard.
"""


def convert_string(input_string):
    number = input_string.count(",") + 1
    output_string = input_string.replace(" ", "").replace("\n", "")
    # replace black " " and "\n"
    # output_string=output_string.replace(",","]")
    output_string = output_string.replace(",", "\n> 1.\n---\n\n> [!WORD]+ ")
    output_string = "> [!WORD]+ " + output_string + "\n> 1.\n---\n\n> [!WORD]+ "
    print(f"There are {number} words")
    return output_string


def string_to_clipboard(string):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, string)
    win32clipboard.CloseClipboard()


if __name__ == '__main__':
    word = input("Enter the word: ")
    word = get_data.Word(word)
    text = markdown.word_markdown(word)
    string_to_clipboard(text)
