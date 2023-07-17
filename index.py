"""
Index creation

Run 1 time only for creating index, must have data in "Data" folder
"""
import glob
import os.path

from whoosh.index import (
    create_in,
    open_dir,
    exists_in,
)
from whoosh.fields import Schema, TEXT

schema = Schema(
    path = TEXT(stored=True),
    title = TEXT(stored=True),
    content = TEXT(stored=True),
)

paths = glob.glob('Data\\*.txt')

if not os.path.exists("Index"):
    os.mkdir("Index")
if exists_in("Index"):
    ix = create_in("Index", schema)
else:
    ix = open_dir("Index")


docs = {}
for path in paths:
    with open(path, encoding="utf-8") as f:
        writer = ix.writer()
        file = f.read()
        print(file)
        try:
            extracted = file.replace("\n\n", "\n").split("\n", 3)
            extracted.pop()
            title, link, content = extracted
            print(title)
            print(link)
            print(content)
            writer.add_document(path=paths[1], title=title, content=content)
            writer.commit()
        except:
            writer.commit()