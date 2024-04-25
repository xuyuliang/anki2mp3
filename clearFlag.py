
from ctypes import sizeof
import json
import os
import sqlite3
import shutil
from bs4 import BeautifulSoup
import html2text



# 假设数据库文件位于 Anki 用户数据目录下，您需要根据实际情况调整路径
# 例如，Windows 系统上的路径可能类似于 'C:\\Users\\YourUsername\\.Anki2\collection.anki2-id\profiles\\default\colpkg.sqlite'
# anki_database_path = r'C:\Users\user\AppData\Roaming\Anki2\User 1\collection.anki2'
tmp_database_path = r'.\mytempanki.db'
# inputfile_path = r".\selectednotes"
# config.ini
import configparser
config = configparser.RawConfigParser()
config.read("config.ini",encoding='utf-8')
anki_database_path = eval(config['folders']['anki_database_path'])
ignore_colors = eval(config['filename']['ignore_filenames'])
inputfile_path = config['folders']['INPUT_FOLDER']
ANKI_FIELDS = (config['Anki_fields']['word'],config['Anki_fields']['tips'],config['Anki_fields']['explanation'],config['Anki_fields']['fullexplanation'])
p_word,p_tip,p_explanation,p_fullexplanation = ANKI_FIELDS
positions = {'word':int(p_word)-1,'tips':int(p_tip)-1,'explanation':int(p_explanation)-1,'fullexplanation':int(p_fullexplanation)-1}
#
def recopy_temp_database():
    #copy to current temp directory
    # if file exist ,delete it
    if os.path.exists(tmp_database_path):
        print("tmp_database exist,delete it")
        os.remove(tmp_database_path)
    shutil.copy(anki_database_path, tmp_database_path)

def find_all_color():
    # 连接到 Anki 的 SQLite 数据库
    conn = sqlite3.connect(anki_database_path)
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()

    # 假设 'cards' 表格中有一个名为 'flags' 的字段，用于标识卡片的颜色
    query1= "select count(*) as cnt from cards where flags != 0"
    query2 = "update cards set flags = 0 where flags != 0"
    try:
        # 执行查询
        cursor1.execute(query1)
        # 获取所有结果
        colors = cursor1.fetchall()
        print("the count of colored(flag) cards:"+str(colors[0][0]))
        # convert to normal list
        cursor2.execute(query2)
        conn.commit()


    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    # 关闭游标和连接
    finally:
        cursor1.close()
        cursor2.close()
        conn.close()
# the main function

def main():
    # backup db
    recopy_temp_database()
    # print(ignore_colors)
    find_all_color()

if __name__ == "__main__":
    main()