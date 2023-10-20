def word_markdown(word):
    """
    Form the markdown text in Obsidian and return text.
    :param word: get_data.Word
    :return: string, Obsidian text
    """
    text = f"\n> [!WORD]+ {word.spelling}    {word.phonetic}    {word.rank}\n"
    for order, trans in enumerate(word.trans_list):
        text += f"> {order + 1}. {trans['property']} {trans['meaning']}\n"
        if trans["example_list"]:
            for example in trans["example_list"]:
                text += f"> \t- e.g. {example['example_EN']} {example['example_CN']}\n"
    text += "---\n"
    return text
