import os
import read,get_data,markdown
date="2022-10-31"
dirct="C:\\Users\\Panhuiming\\iCloudDrive\\iCloud~md~obsidian\\Obsidian\\5-Daily\\3-English"
filename=f"draft English {date}.md"

path=os.path.join(dirct,filename)

words = read.read_words("file", path= "test\\test.txt", filetype="zotero")
with open(path,encoding="utf-8",mode="w+") as f:
    for word in words:
        try:
            word=get_data.Word(word)
        except:
            continue
        word_text=markdown.word_markdown(word)
        f.write(word_text)

f.close()