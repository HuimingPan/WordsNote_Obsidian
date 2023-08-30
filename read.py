import re


def read_words(source: str, **par):
    """
    Select proper function to obtain the words and pass the corresponding parameters. Return the words list.
    :param source: The way to pass the original string containing the words. It can be "file", "pasted" ...
    :param par: The parameters needed in sub-function like read_words_from_file.
    :return: A list containing words to be looked up.
    """
    if source == "file":
        return read_words_from_file(**par)


def read_words_from_file(path: str, filetype: str):
    """
    Obtain the words to be looked up from a txt file which contains the text copied from zotero.
    :param path: The path where the file locates.
    :return: A list containing words, for example ["word","vocabulary"].
    """
    if filetype=="zotero":
        reg = '“([a-z]+)”'
    elif filetype=="foxitPDF":
        reg = r'([a-z]+)\n'
    reg = re.compile(reg)
    with open(path, encoding="utf-8") as f:
        # 正则表达式的使用
        original_text = f.read()
        f.close()
        return reg.findall(original_text)
