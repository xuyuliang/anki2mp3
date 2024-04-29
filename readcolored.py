# from ctypes import sizeof
import json
import os
import sqlite3
import shutil
from bs4 import BeautifulSoup



# 假设数据库文件位于 Anki 用户数据目录下，您需要根据实际情况调整路径
# 例如，Windows 系统上的路径可能类似于 'C:\\Users\\YourUsername\\.Anki2\collection.anki2-id\profiles\\default\colpkg.sqlite'
# anki_database_path = r'C:\Users\user\AppData\Roaming\Anki2\User 1\collection.anki2'
# tmp_database_path = r".\mytempanki.db"
tmp_database_path = "mytempanki.db"
# inputfile_path = r".\selectednotes"
# config.ini
import configparser
config = configparser.RawConfigParser()
config.read("config.ini",encoding='utf-8')
anki_database_path = '' 
ignore_colors = eval(config['filename']['ignore_filenames'])
inputfile_path = config['folders']['INPUT_FOLDER']
ANKI_FIELDS = (config['Anki_fields']['word'],config['Anki_fields']['tips'],config['Anki_fields']['explanation'],config['Anki_fields']['fullexplanation'])
p_word,p_tip,p_explanation,p_fullexplanation = ANKI_FIELDS
positions = {'word':int(p_word)-1,'tips':int(p_tip)-1,'explanation':int(p_explanation)-1,'fullexplanation':int(p_fullexplanation)-1}
#
def determin_anki_database_path():
    paths = eval(config['folders']['anki_database_path'])
    # print('paths:',paths)
    for path in paths:
        if os.path.isfile(path):
           global anki_database_path 
           anki_database_path = path
        #    print(anki_database_path)
           break


def recopy_temp_database():
    #copy to current temp directory
    # if file exist ,delete it
    if os.path.exists(tmp_database_path):
        print("tmp_database exist,delete it")
        os.remove(tmp_database_path)
    shutil.copy(anki_database_path, tmp_database_path)

def find_all_color():
    # 连接到 Anki 的 SQLite 数据库
    conn = sqlite3.connect(tmp_database_path)
    cursor = conn.cursor()

    # 假设 'cards' 表格中有一个名为 'flags' 的字段，用于标识卡片的颜色
    query = "SELECT distinct flags from cards where flags != 0"
    try:
        # 执行查询
        cursor.execute(query)
        # 获取所有结果
        colors = cursor.fetchall()
        # convert to normal list
        result_list = []
        for color in colors:
            result_list.append(color[0])
        print(colors)
        print(result_list)
        return result_list


    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    # 关闭游标和连接
    finally:
        cursor.close()
        conn.close()
def export_json_by_color(color):

    # 连接到 Anki 的 SQLite 数据库
    conn = sqlite3.connect(tmp_database_path)
    cursor = conn.cursor()

    # 假设 'cards' 表格中有一个名为 'flags' 的字段，用于标识卡片的颜色
    query = f"SELECT n.flds from notes as n INNER JOIN cards as c on n.id = c.nid where c.flags == {color}"

    try:
        # 执行查询
        cursor.execute(query)
        # 获取所有结果
        blue_cards = cursor.fetchall()
        # 输出找到的某色卡片信息
        inputfile = os.path.join(inputfile_path,str(color)+'.json')
        if os.path.exists(inputfile):
            os.remove(inputfile)
            print("inputfile exist,delete it")
        file2 = open(inputfile,'w',encoding='utf-8')
        outerlist = []
        for card in blue_cards:
            print('type of blue_cards',type(card))
            print('a card:',len(card))
            flds = card[0].split('')
            sn = 0
            dictlist = []
            for fld in flds:
                if sn == 0:
                    print(fld)
                fldtext =BeautifulSoup(fld, 'html.parser').get_text(separator=" ")
                dictlist.append({sn:fldtext})            
                sn += 1
            outerlist.append(dictlist)
            # print(outerlist)
        json.dump(outerlist, file2, ensure_ascii=False, indent=4)
        file2.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    # 关闭游标和连接
    cursor.close()
    conn.close()
# the main function

def main():
    determin_anki_database_path()
    recopy_temp_database()
    # print(ignore_colors)
    allcolors = find_all_color()
    colors_todo = list(set(allcolors) - set(ignore_colors))
    for color in colors_todo:
        export_json_by_color(color)

if __name__ == "__main__":
    main()