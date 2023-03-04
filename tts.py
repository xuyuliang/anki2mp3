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
LONGMAN_BASE_PATH = config['folders']['LONGMAN_BASE_PATH']
INPUT_FOLDER= config['folders']['INPUT_FOLDER']
NEED_READ_SPELLING = False
# wordpair = {}
# for item in config['symbol_pronounce']:
#     print(item)
#     wordpair.update(item[0][1:-1],item[1][1:-1])
# print(wordpair)
SYMBOL_REPLACE ={}


# print (SYMBOL_REPLACE) 
def find_sound_of_word(word) :
    pass


def symboltocn(currword,text):
    # wordpair = {}
    # wordpair.update( {'=>':'衍生','~=':'约等于','SYN':'同义词','%=':'约等于','=>':'衍生 '} )
    # wordpair.update( {'OPP':'反义词','=':'同义词','%':currword+' ','~':currword+' ',':':'.'} )
    # wordpair.update( {'BrE':'英国英语','NAmE':'美国英语','\n':'.','adj.':'。adjective。','n.':'。noun。','vt.':'。vt.'} )
    # wordpair.update( {'vi.':'。vi.','adv.':'。adverb.','v.':'。v.','sb.':'somebody','sth.':'something'} )
    # wordpair.update( {' sb':'。somebody',' sth':'。something',':(':'。(',':)':'。)'} )
    for item in config['symbol_pronounce']:
        curr = config['symbol_pronounce'][item]
        SYMBOL_REPLACE.update(eval(curr))
    for k,v in SYMBOL_REPLACE.items():
        text = text.replace(k,v)
    return text

def processInputFile(input_file):

    file = open(os.path.join(INPUT_FOLDER, input_file), "r",encoding='utf-8')
    # file = open(input_file, "r",encoding='latin-1')
    textlist = [] 
    lyric =[]
    for line in file:
        content = [] 
        word_and_tips = {}
        word = line.split("\t")[0]
        letters = cutwords.cutbypronuncation(word) 
        word_and_tips['word'] = word
        if NEED_READ_SPELLING:
            word_and_tips['spelling'] = letters 
        word_and_tips['tips'] = line.split("\t")[6]
        lyric.append(word_and_tips)
        explain = line.split("\t")[2]
        explain = symboltocn(word,explain)
        words =  (word +'. ')*3
        mydict = {}
        mydict['en']=words
        content.append(mydict)
        if NEED_READ_SPELLING:
            mydict = {}
            mydict['spelling']=letters
            content.append(mydict)
        mydict = {}
        mydict['cn']=explain
        content.append(mydict)
        
        mydict = {}
        mydict['en']=words
        content.append(mydict)

        textlist.append(content)
    file.close
    return textlist,lyric

def list_voices(engine):
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.id)

    # quit()
def read_spelling(engine,filename,aword):
    currpath = os.path.join(SOUND_TEMP_FOLDER,filename)
    aword= str.strip(aword.split('.')[0]) #因为TTS默认念3遍，words已经预处理了 * 3
    engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
    engine.setProperty("rate", 100)
    newword = cutwords.cutbypronuncation(aword) 
    # newword = list(newword)
    # newword = ' '.join(newword)
    engine.save_to_file(newword,currpath)
    print('read spelling',newword,currpath)
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
    elif sound_source=='longman':
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
                print(word,'在longman 库中找不到，只好tts')
                engine.setProperty("rate", 100)
                engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
                engine.save_to_file(v,currpath)
                engine.runAndWait()

            cur.close()
            con.close()

        if k=='spelling':
            engine.setProperty("rate", 200)
            engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
            engine.save_to_file(v,currpath)
            engine.runAndWait()
        if k=='cn':
            engine.setProperty("rate", 150)
            engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
            engine.save_to_file(v,currpath)
            engine.runAndWait()

    else:
        if k=='en':
            engine.setProperty("rate", 100)
            engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
            engine.save_to_file(v,currpath)
            engine.runAndWait()
        if k=='spelling':
            engine.setProperty("rate", 200)
            engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
            engine.save_to_file(v,currpath)
            engine.runAndWait()
        if k=='cn':
            engine.setProperty("rate", 150)
            engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
            engine.save_to_file(v,currpath)
            engine.runAndWait()

def merge_sound(output_filename,lyriclist):
    tempmp3_path,outputmp3_path = SOUND_TEMP_FOLDER , SOUND_OUTPUT_FOLDER
    mp3_files = [file for file in os.listdir(tempmp3_path) if file.endswith(".mp3") and file[:-4].isdigit()]
    mp3_files.sort(key=lambda x: int(x[:-4]))
    combined = AudioSegment.empty()
    total_duration = 0
    i = 0
    j = 0
    t = datetime.datetime.now()
    # export_filename = str(t).split('.')[0].replace(' ','日').replace(':','-') +'.mp3'
    # export_lyric = str(t).split('.')[0].replace(' ','日').replace(':','-') +'.lrc'
    export_filename = output_filename.split('.')[0] +'.mp3'
    export_lyric = output_filename.split('.')[0] +'.lrc'
        
    file_lrc = open(os.path.join(outputmp3_path, export_lyric), "w",encoding='utf-8')
    file_lrc.write('[re:CompuPhase XYL]\n\n')
    m,s,ms = (0,0,0)
    if NEED_READ_SPELLING:
        for mp3_file in mp3_files:

            currtime = str(f"[{int(m):02d}:{int(s):02d}.{ms}]")
            if i%4 == 0:
                # currtext = lyriclist[j]['word']+'\n'+lyriclist[j]['tips']+'\n'
                currtext = lyriclist[j]['word']+'\n'
                # j+=1
                file_lrc.write(currtime+currtext)
            if i%4 == 1:
                currtext = lyriclist[j]['spelling']+'\n'
                # j+=1
                file_lrc.write(currtime+currtext)
            if i%4 == 2:
                currtext = lyriclist[j]['tips']+'\n'
                # j+=1
                file_lrc.write(currtime+currtext)
            if i%4 == 3:
                currtext = lyriclist[j]['word']+'\n'
                j+=1
                file_lrc.write(currtime+currtext)
            i+=1
            currfile = os.path.join(tempmp3_path, mp3_file)
            # sound = AudioSegment.from_file(currfile, format="mp3")
            sound = AudioSegment.from_file(currfile)
            duration_sec = sound.duration_seconds
            total_duration += duration_sec
            print('合并',currfile,'时长:',duration_sec)
            combined += sound
            m, s = divmod(total_duration, 60)
            ms = str(total_duration - int(total_duration))[2:4]

    else:
        for mp3_file in mp3_files:

            currtime = str(f"[{int(m):02d}:{int(s):02d}.{ms}]")
            if i%3 == 0:
                # currtext = lyriclist[j]['word']+'\n'+lyriclist[j]['tips']+'\n'
                currtext = lyriclist[j]['word']+'\n'
                # j+=1
                file_lrc.write(currtime+currtext)
            if i%3 == 1:
                currtext = lyriclist[j]['tips']+'\n'
                # j+=1
                file_lrc.write(currtime+currtext)
            if i%3 == 2:
                currtext = lyriclist[j]['word']+'\n'
                j+=1
                file_lrc.write(currtime+currtext)
            i+=1
            currfile = os.path.join(tempmp3_path, mp3_file)
            # sound = AudioSegment.from_file(currfile, format="mp3")
            sound = AudioSegment.from_file(currfile)
            duration_sec = sound.duration_seconds
            total_duration += duration_sec
            print('合并',currfile,'时长:',duration_sec)
            combined += sound
            m, s = divmod(total_duration, 60)
            ms = str(total_duration - int(total_duration))[2:4]

    file_lrc.close()
    combined.export(os.path.join(outputmp3_path,export_filename), format="mp3")

def product_sound_separately(textlist,input_filename,engine,sound_source='localTTS'):
    # engine.setProperty("voice", engine.getProperty("voices")[0].id)
    # engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
    # engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Brian22')
    # engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')

    progressfile = 'get_sound_progress'+input_filename.split('.')[0]+'.txt'
    file_ori_list_dict = csv.writer(open(os.path.join(SOUND_OUTPUT_FOLDER, progressfile), "w",encoding='utf-8'))
    i = 1
    for contents in textlist:
        # print(contents)
        # print('-----------')
        file_ori_list_dict.writerow(contents)
        for content in contents:
            print(content)
            for k,v in content.items():
                print(k,v)
                print('-------')
                text_to_sound(k,v,engine,str(i)+'.mp3',sound_source)
                i+=1

def clean_list(textlist):
    testfile = open('./testfile.txt',"w",encoding='utf-8')
    textlistlatin1 = []
    morepunctuations ='”’‘“'
    for item in textlist:
        item.replace('\\\\','.')
        item.replace('\n','.')

        item.replace('"','.')
        item.replace("'",'.')
        item.replace('`','.')
        newitem = item.translate(str.maketrans("","", string.punctuation+morepunctuations))
        # textlistlatin1.append(item.encode('latin-1'))
        textlistlatin1.append(newitem)
        print(newitem)
        testfile.write(newitem+'\n')
    testfile.close
    return textlistlatin1

def clear_sound_folder(sound_folder):
    for file_object in os.listdir(sound_folder):
        file_object_path = os.path.join(sound_folder, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        # else:
        #     shutil.rmtree(file_object_path)

def main():
    engine = pyttsx3.init()
    engine.setProperty("stripPunct",True)
    engine.setProperty("rate", 100)
    engine.setProperty("volume", 1.2)
    # list_voices(engine)
    for input_file in os.listdir(INPUT_FOLDER):
        if not os.path.isfile(os.path.join(INPUT_FOLDER,input_file)):
            continue
        print(type(input_file),':',input_file)
        if config['filename']['spelling_difficulty'] in input_file:
            global NEED_READ_SPELLING
            NEED_READ_SPELLING = True 
        textlist,lyriclist = processInputFile(input_file)
        clear_sound_folder(SOUND_TEMP_FOLDER)
        product_sound_separately(textlist,input_file,engine,sound_source='longman')
        merge_sound(input_file,lyriclist)
    

    

if __name__ == "__main__":
    main()