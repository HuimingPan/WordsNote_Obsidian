import os
location="D:\\OneDrive - whu.edu.cn\\Others\Obsidian\\5-Daily\\3-English"


def word_markdown(word):
    number_trans=len(word.trans_list)
    text=text=f"\n> [!WORD]+ {word.spelling}    {word.phonetic}    {word.rank}\n"
    for order,trans in enumerate(word.trans_list):
        text+=f"> {order+1}. {trans['property']} {trans['meaning']}\n"
        if trans["example_list"]:
            for example in trans["example_list"]:
                text+=f"> \te.g. {example['example_EN']} {example['example_CN']}\n"
    text+="---\n"
    return text
