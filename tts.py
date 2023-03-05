import datetime
import os
import shutil
import sqlite3
import string
import pyttsx3
import gtts
import csv
import configparser
import cutwords
from pydub import AudioSegment

config = configparser.RawConfigParser()
config.read("config.ini",encoding='utf-8')
SOUND_TEMP_FOLDER = config['folders']['SOUND_TEMP_FOLDER']
SOUND_OUTPUT_FOLDER = config['folders']['SOUND_OUTPUT_FOLDER']
INPUT_FOLDER= config['folders']['INPUT_FOLDER']
CN_ENGINE = config['engines']['cn'] 
EN_ENGINE = config['engines']['en'] 
SPELLING_ENGINE = config['engines']['spelling'] 
ANKI_FIELDS = (config['Anki_fields']['word'],config['Anki_fields']['tip'],config['Anki_fields']['explanation'])
NEED_READ_SPELLING = False
SYMBOL_REPLACE ={}
LONGMAN_BASE_PATH = '' 

def determin_LONGMAN_BASE_PATH():
    paths = eval(config['folders']['LONGMAN_BASE_PATH'])
    print(paths)
    for path in paths:
        if os.path.isdir(path):
           global LONGMAN_BASE_PATH
           LONGMAN_BASE_PATH = path
           break


def symboltocn(currword,text):
    for item in config['symbol_pronounce']:
        curr = config['symbol_pronounce'][item]
        global SYMBOL_REPLACE
        SYMBOL_REPLACE.update(eval(curr))
    for k,v in SYMBOL_REPLACE.items():
        text = text.replace(k,v)
    return text

def processInputFile(input_file):
    p_word,p_tip,p_explanation = ANKI_FIELDS
    file = open(os.path.join(INPUT_FOLDER, input_file), "r",encoding='utf-8')
    textlist = [] 
    lyric =[]
    for line in file:
        # process lyric
        word_and_tips = {}
        word = line.split("\t")[int(p_word)-1]
        word_and_tips['word'] = word
        tips = line.split("\t")[int(p_tip)-1];
        if NEED_READ_SPELLING:
            letters = cutwords.extract_english_letters(word,tips)
            if letters == '':
                letters = cutwords.cutbypronuncation(word) 
            word_and_tips['spelling'] = letters 
        word_and_tips['tips'] = tips
        word_and_tips['word_again'] = word
        lyric.append(word_and_tips)

        # process textlist
        content = [] 
        words =  (word +'. ')*3
        mydict = {}
        mydict['en']=words
        content.append(mydict)

        if NEED_READ_SPELLING:
            mydict = {}
            mydict['spelling']=letters
            content.append(mydict)

        mydict = {}
        explain = line.split("\t")[int(p_explanation)-1]
        explain = symboltocn(word,explain)
        mydict['cn']=explain
        content.append(mydict)
        
        mydict = {}
        mydict['en']=words
        content.append(mydict)

        textlist.append(content)
    file.close
    return textlist,lyric
def text2mp3(type,engine,path,v):

    if type == 'en':
        engine.setProperty("rate", 100)
        engine.setProperty('voice',EN_ENGINE)
    if type == 'spelling':
        engine.setProperty("rate", 100)
        engine.setProperty('voice',SPELLING_ENGINE)
    if type == 'cn':
        engine.setProperty("rate", 150)
        engine.setProperty('voice',CN_ENGINE)
    engine.save_to_file(v,path)
    engine.runAndWait()
def text_to_sound(k,v,engine,filename,sound_source):
    currpath = os.path.join(SOUND_TEMP_FOLDER,filename)
    print(currpath)
    if sound_source=='gTTS':
        if k=='en':
            tts = gtts.gTTS(v,lang="en")
            tts.save(currpath)
        if k=='spelling':
            tts = gtts.gTTS(v,lang="en")
            tts.save(currpath)
        if k=='cn':
            tts = gtts.gTTS(v,lang="zh")
            tts.save(currpath)
    if sound_source=='longman':
        if k=='en':
            con= sqlite3.connect("./sound_vocabulary.db")
            cur= con.cursor()
            word= str.strip(v.split('.')[0]) #因为TTS默认念3遍，words已经预处理了 * 3
            # print(word)
            cur.execute('select pathname,filename from wordslocation where word=? and attrib="BRI"', (word,))
            row = cur.fetchone()
            if row != None:
                shutil.copyfile(os.path.join(LONGMAN_BASE_PATH,row[0],row[1]),currpath)
            else:
                print(word,'在longman 库中找不到 只好tts')
                text2mp3('spelling',engine,currpath,v)
            cur.close()
            con.close()
        else:
            text2mp3(k,engine,currpath,v)

    if sound_source == 'localTTS':
        text2mp3(k,engine,currpath,v)

def merge_sound(input_filename,lyriclist):
    tempmp3_path,outputmp3_path = SOUND_TEMP_FOLDER , SOUND_OUTPUT_FOLDER
    mp3_files = [file for file in os.listdir(tempmp3_path) if file.endswith(".mp3") and file[:-4].isdigit()]
    mp3_files.sort(key=lambda x: int(x[:-4]))
    combined = AudioSegment.empty()
    total_duration = 0
    export_filename = input_filename.split('.')[0] +'.mp3'
    export_lyric = input_filename.split('.')[0] +'.lrc'
        
    file_lrc = open(os.path.join(outputmp3_path, export_lyric), "w",encoding='utf-8')
    file_lrc.write('[re:CompuPhase XYL]\n\n')
    m,s,ms = (0,0,0)
    #
    # print('len of list',len(lyriclist))
    # print('len of mp3files',len(mp3_files))
    i = 0
    for dictitem in lyriclist:
        print(i,dictitem)
        for currkey in dictitem: 
            print(currkey)
            #lyric
            currtime = str(f"[{int(m):02d}:{int(s):02d}.{ms}]")
            currtext = dictitem[currkey]+'\n'
            file_lrc.write(currtime+currtext)
            #mp3
            mp3_file = mp3_files[i]
            currfile = os.path.join(tempmp3_path, mp3_file)
            sound = AudioSegment.from_file(currfile)
            duration_sec = sound.duration_seconds
            total_duration += duration_sec
            print('合并',currfile,'时长:',duration_sec)
            combined += sound
            m, s = divmod(total_duration, 60)
            ms = str(total_duration - int(total_duration))[2:4]
            i+=1

    file_lrc.close()
    combined.export(os.path.join(outputmp3_path,export_filename), format="mp3")

def product_sound_separately(textlist,input_filename,engine,sound_source='localTTS'):

    progressfile = 'get_sound_progress'+input_filename.split('.')[0]+'.txt'
    file_ori_list_dict = csv.writer(open(os.path.join(SOUND_OUTPUT_FOLDER, progressfile), "w",encoding='utf-8'))
    i = 1
    for contents in textlist:
        file_ori_list_dict.writerow(contents)
        for content in contents:
            print(content)
            for k,v in content.items():
                print(k,v)
                print('-------')
                text_to_sound(k,v,engine,str(i)+'.mp3',sound_source)
                i+=1


def clear_sound_folder(sound_folder):
    for file_object in os.listdir(sound_folder):
        file_object_path = os.path.join(sound_folder, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.remove(file_object_path)
        else:
            shutil.rmtree(file_object_path)

def main():
    engine = pyttsx3.init()
    engine.setProperty("stripPunct",True)
    engine.setProperty("rate", 100)
    engine.setProperty("volume", 1.2)
    # list_voices(engine)
    determin_LONGMAN_BASE_PATH()
    for input_file in os.listdir(INPUT_FOLDER):
        if not os.path.isfile(os.path.join(INPUT_FOLDER,input_file)):
            continue
        if config['filename']['spelling_difficulty'] in input_file:
            global NEED_READ_SPELLING
            NEED_READ_SPELLING = True 
        else:
            NEED_READ_SPELLING = False
        textlist,lyriclist = processInputFile(input_file)
        clear_sound_folder(SOUND_TEMP_FOLDER)
        product_sound_separately(textlist,input_file,engine,sound_source='longman')
        merge_sound(input_file,lyriclist)
    

    

if __name__ == "__main__":
    main()
    # determin_LONGMAN_BASE_PATH()