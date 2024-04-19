import ast
import datetime
# import html2text
import json
import os
import re
import shutil
import sqlite3
import pyttsx3
from testEdgeTTS import process_text 
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
EXPLAIN_ENGINE = config['engines']['explanation'] 
WORD_ENGINE = config['engines']['word'] 
SPELLING_ENGINE = config['engines']['spelling'] 
ANKI_FIELDS = (config['Anki_fields']['word'],config['Anki_fields']['tips'],config['Anki_fields']['explanation'],config['Anki_fields']['fullexplanation'])
SYMBOL_REPLACE ={}
LONGMAN_BASE_PATH = '' 

# print('totally_forget' in config['customized'])
# print(type(config['customized']))

def determin_LONGMAN_BASE_PATH():
    paths = eval(config['folders']['LONGMAN_BASE_PATH'])
    print(paths)
    for path in paths:
        if os.path.isdir(path):
           global LONGMAN_BASE_PATH
           LONGMAN_BASE_PATH = path
           break

# parse a cvs file , ignore lines begin with '#' ,print every line




def symboltocn(currword,text):
    for item in config['symbol_pronounce']:
        curr = config['symbol_pronounce'][item]
        global SYMBOL_REPLACE
        SYMBOL_REPLACE.update(eval(curr))
    for k,v in SYMBOL_REPLACE.items():
        text = text.replace(k,v)
    return text

def analyse_filename(filename):
    read_order=[{}]
    lyric_order = [{}]
    option = ''
    filename = filename.split('.')[0]

    for item in config['filename']:
        if filename == config['filename'][item]:
            option = item  
    if option == '':
        option = 'default'
    # print('option:',option)
    if option in config['customized']:
        read_order = eval(config['customized'][option])['read']
        lyric_order = eval(config['customized'][option])['lyric']
    else:
        option = 'default'
        read_order = eval(config['customized'][option])['read']
        lyric_order = eval(config['customized'][option])['lyric']

    return (read_order,lyric_order)
def detect_hash_with_spaces(string):
  """Returns True if the string begins with a # character, including spaces."""

  # Compile the regular expression pattern.
  pattern = re.compile(r'^[ \t]*#') 

  # Match the pattern against the string.
  match = pattern.match(string)

  # Return True if there is a match, False otherwise.
  return match is not None

def processInputFile(input_file):
    p_word,p_tip,p_explanation,p_fullexplanation = ANKI_FIELDS
    positions = {'word':int(p_word)-1,'tips':int(p_tip)-1,'explanation':int(p_explanation)-1,'fullexplanation':int(p_fullexplanation)-1}
    file = open(os.path.join(INPUT_FOLDER, input_file), "r",encoding='utf-8')
    readlist = [] 
    lyriclist =[]
    read_order,lyric_order =  analyse_filename(input_file)
    # print(read_order)
    # print(lyric_order)
    # input()
    # print(input_file)
    outerlist = json.load(file)
    for notefields in outerlist:
        # print(notefields)
        # a = str(positions['word'])
        word = notefields[positions['word']][str(positions['word'])]
        # a='0'
        # word = notefields[positions['word']][a]
        print("============")
        print(word)
        # word = notefields[positions['word']]['1']
        tips = notefields[positions['tips']][str(positions['tips'])]
        explain = notefields[positions['explanation']][str(positions['explanation'])]
        full_explain = notefields[positions['fullexplanation']][str(positions['fullexplanation'])]


        # get letters
        # letters = cutwords.extract_english_letters(word,tips)
        letters = cutwords.extract_english_letters(word,tips)
        if letters == '':
            # letters = ' '.join(list(cutwords.cutbyroot2(word)))
            letters =  cutwords.extract_english_letters(word,full_explain)
            if letters == '': # if no . there , means it's a one syllabel word or just get nothing ,then try use the word as it is.
                if len(word) < 7:
                    letters = word
                    letters = ' '.join(list(word))
                else:
                    letters = ' '.join(list(cutwords.cutbyroot2(word)))
        # process lyric
        aline_lyric = []
        for item in lyric_order:
            if item == 'spelling':
                aline_lyric.append({'spelling':letters})
            else:
                aline_lyric.append({item:notefields[positions[item]][str(positions[item])]})
        print('lylic begin')
        print(aline_lyric)
        print('lylic end')
        lyriclist.append(aline_lyric)

        # process textlist
        aline_readtext = []
        for item in read_order:
            if item == 'word':
                # replace '.' with ' ' in item becauce of some bug in somewhere I don't know.
                word = word.replace('.',' ')
                aline_readtext.append({'word':(word +'. ')*3})
            if item == 'explanation':
                # read as html
                explain = symboltocn(word,explain)
                aline_readtext.append({'explanation':explain})
            if item == 'spelling':
                aline_readtext.append({'spelling':letters})
            # else:
            #     aline_readtext.append({item:notefields[positions[item]]})
        readlist.append(aline_readtext)
            
    file.close
    print(readlist)
    print(lyriclist)
    return readlist,lyriclist
def text2mp3(type,engine,path,v):

    if type == 'word':
        engine.setProperty("rate", 120)
        engine.setProperty("volumn", 1.2)
        engine.setProperty('voice',WORD_ENGINE)
    if type == 'spelling':
        engine.setProperty("rate", 120)
        engine.setProperty("volumn", 1)
        engine.setProperty('voice',SPELLING_ENGINE)
    if type == 'explanation':
        engine.setProperty("rate", 150)
        engine.setProperty("volumn", 1)
        engine.setProperty('voice',EXPLAIN_ENGINE)
    engine.save_to_file(v,path)
    engine.runAndWait()


def text_to_sound(k,v,engine,filename,sound_source):
    currpath = os.path.join(SOUND_TEMP_FOLDER,filename)
    print(currpath)
    if sound_source=='gTTS':
        if k=='word':
            tts = gtts.gTTS(v,lang="en")
            tts.save(currpath)
        if k=='spelling':
            tts = gtts.gTTS(v,lang="en")
            tts.save(currpath)
        if k=='explanation':
            tts = gtts.gTTS(v,lang="zh")
            tts.save(currpath)
    if sound_source=='edge':
        if k=='word':
            process_text(v,currpath)
        else:
            text2mp3(k,engine,currpath,v)
    if sound_source=='longman':
        if k=='word':
            con= sqlite3.connect("./sound_vocabulary.db")
            cur= con.cursor()
            word= str.strip(v.split('.')[0]) #因为TTS默认念3遍，words已经预处理了 * 3
            # print(word)
            cur.execute('select pathname,filename from wordslocation where word=? and attrib="BRI"', (word,))
            row = cur.fetchone()
            if row != None:
                shutil.copyfile(os.path.join(LONGMAN_BASE_PATH,row[0],row[1]),currpath)
                combined = AudioSegment.empty()
                sound = AudioSegment.from_file(currpath)
                combined = sound * 2
                combined.export(currpath, format="mp3")
            else:
                print(word,'在longman 库中找不到 只好tts')
                text2mp3('spelling',engine,currpath,v)
            cur.close()
            con.close()
        else:
            text2mp3(k,engine,currpath,v)

    if sound_source == 'localTTS':
        text2mp3(k,engine,currpath,v)



def merge_sound(input_filename,readlist,lyriclist):
    tempmp3_path,outputmp3_path = SOUND_TEMP_FOLDER , SOUND_OUTPUT_FOLDER
    mp3_files = [file for file in os.listdir(tempmp3_path) if file.endswith(".mp3") and file[:-4].isdigit()]
    mp3_files.sort(key=lambda x: int(x[:-4]))
    combined = AudioSegment.empty()
    total_duration = 0
    export_filename = input_filename.split('.')[0] +'.mp3'
    export_lyric = input_filename.split('.')[0] +'.lrc'
        
    file_lrc = open(os.path.join(outputmp3_path, export_lyric), "w",encoding='utf-8')
    file_lrc.write('[ar:XYL]\n')
    file_lrc.write('[ti:'+input_filename.split('.')[0]+']\n')
    m,s,ms = (0,0,0)
    #
    # print('len of list',len(lyriclist))
    # print('len of mp3files',len(mp3_files))
    i = 0
    lyric_item = 0
    for line in readlist:
        print(i,line)
        j = 0
        for currdict in line: 
            print(currdict)
            #lyric
            currtime = str(f"[{int(m):02d}:{int(s):02d}.{ms}]")
            # print("当前list是：", list(lyriclist[lyric_item]))

            if j < len( lyriclist[lyric_item] ):
               for key,currtext in lyriclist[lyric_item][j].items():
                   currtext = currtext + '\n'
               j+=1
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
        lyric_item += 1
    file_lrc.close()
    combined.export(os.path.join(outputmp3_path,export_filename), format="mp3")

def product_sound_separately(readlist,input_filename,engine,sound_source='localTTS'):

    progressfilename = 'get_sound_progress'+input_filename.split('.')[0]+'.json'
    # check if the file exists
    progressfile = os.path.join(SOUND_OUTPUT_FOLDER, progressfilename)
    if os.path.exists(progressfile)  :
        print('old file exist, delete it')
        os.remove(progressfile)

    # create progressfile
    f = open(progressfile, "w",encoding='utf-8')
    with f:
        json.dump(readlist, f, ensure_ascii=False, indent=4)
    f.close()


    # input(progressfile+'has created,you can manully modify it'+' press enter to continue')
    i = 1
    file_ori_list_dict = []
    # read from the file, create seperated mp3s
    file_ori_list_dict = json.load(open(progressfile, "r",encoding='utf-8'))
    for line in file_ori_list_dict:
        for content in line:
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
    engine.setProperty("volume", 1.4)
    # list_voices(engine)
    determin_LONGMAN_BASE_PATH()
    for input_file in os.listdir(INPUT_FOLDER):
        if not os.path.isfile(os.path.join(INPUT_FOLDER,input_file)):
            continue
        readlist,lyriclist = processInputFile(input_file)
        clear_sound_folder(SOUND_TEMP_FOLDER)
        # product_sound_separately(readlist,input_file,engine)
        product_sound_separately(readlist,input_file,engine,sound_source='longman')
        merge_sound(input_file,readlist,lyriclist)
    # program normally finished
    print("program normally finished, have a nice day")
    print("press 'Enter' key to exit")
    # wait for user input
    input()
    engine.stop()
    
    

    

if __name__ == "__main__":
    main()