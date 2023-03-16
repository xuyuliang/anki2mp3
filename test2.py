import os
import sys
import anki
from anki import Collection
from anki import aqt

# open anki database and open a deck named '双向' and filter 'rated:1:1'
# open anki i
deck = aqt.mw.col.decks.byName('双向')
db = anki.storage.Collection()

# filter by 'rated:1:1'
db.decks.select(deck['id'])
# export to csv
db.exportCSV(os.path.join(os.path.expanduser('~'), 'Desktop', 'test.csv'))  # 将数据导出到csv文件   
# import csv
# with open('test.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)
# quit()
# import csv
# with open('test.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)
# quit()

