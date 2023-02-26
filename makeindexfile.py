import csv
import os
from playsound import playsound
import sqlite3
PATH = r"E:.\朗文直排\sent_rename\sent_rename"



def prepare_csv_row(row):
        foldername = row[0]
        filename = row[1]
        sp_filename = filename.split(' ')
        index = sp_filename[0]
        word = sp_filename[1:-1]
        # print('word:',word)
        if '-' in word:
            attrib = 'sentence'
            range = word.index('-')
            realword =''
            for item in word[0:range]:
                realword = str.strip(realword +' '+ item)
        else:
            attrib = sp_filename[-1].split('.')[0]
            realword =''
            for item in word:
                realword = str.strip(realword +' '+ item)
        # print("realword:",realword,len(realword))
        # if sp_filename[2+i] == '-':
        # print("index,word,attrib,foldername,filename",index,realword,attrib,foldername,filename)
        return{'index':index,'word':realword,'attrib':attrib,'foldername':foldername,'filename':filename}
        # apath =os.path.join(PATH,foldername,filename)
        # playsound(apath)


def main():
    con = sqlite3.connect("./sound_vocabulary.db")
    cur = con.cursor()


    with open('data.csv','r',newline='',encoding='utf-8') as f:
        datacsv = csv.reader(f,delimiter=',')
        # startline=27249
        # endline=27255
        # startline=168550
        # endline=168566
        startline=1
        endline=999999
        i = 1 
        for row in datacsv:
            if i <= startline:
                i = i + 1
                continue 
            mydict = prepare_csv_row(row)
            data = (int(mydict['index']),mydict['word'],mydict['attrib'],mydict['foldername'],mydict['filename'])
            cur.execute("insert into wordslocation(id,word,attrib,pathname,filename) values(?,?,?,?,?)",data)
            print(mydict)
            i=i+1
            if i > endline:
                print('超过预定endline,非正常退出了')
                quit()
            if i % 5000 == 0:
                con.commit()
    con.commit()
    con.close()
if __name__ == "__main__":
    main()