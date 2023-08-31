import os, datetime, json
import read, get_data, markdown

date = datetime.date.today().strftime("%Y-%m-%d")
with open('info.json') as json_file:
    dir_info = json.load(json_file)
    obsidian_dir = dir_info["obsidian_dir"]
    file_dir = dir_info["English_dir"]
filename = f"draft English {date}.md"
path = os.path.join(obsidian_dir, file_dir, filename)

word_source = "clipBoard"
words = read.read_words("file", path="test\\test.txt", filetype=word_source)


with open(path, encoding="utf-8", mode="w+") as f:
    for word in words:
        try:
            word = get_data.Word(word)
        except:
            continue
        word_text = markdown.word_markdown(word)
        f.write(word_text)
f.close()
