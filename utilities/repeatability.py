"""
In this file, we define two functions.
The first one is to append the recorded word in to a file with the date it was first recorded.
The sencond one is to check if the word has been recorded before.
"""

import datetime
import json
import os
import pandas as pd
parameters = json.load(open('info.json'))


def append_word(word_list):
    """
    Append the word to the file with the date it was first recorded.
    """
    date = datetime.date.today().strftime("%Y-%m-%d")
    filename = parameters["history_filename"]
    path = os.path.join("./storage", filename)
    with open(path, encoding="utf-8", mode="a+") as f:
        for word in word_list:
            f.write(f"{word}, {date}\n")


def check_word(word_list):
    """
    Check if the word has been recorded before.
    :param word_list:
    :return:
    """
    filename = parameters["history_filename"]
    path = os.path.join("storage", filename)
    df = pd.read_csv(path, encoding="utf-8", header=None, names=["word", "date"])
    recorded_word_list = df["word"].tolist()
    date_list = df["date"].tolist()
    word_repeat_list = [(word, date_list[recorded_word_list.index(word)]) for word in word_list if word in recorded_word_list]
    return word_repeat_list
