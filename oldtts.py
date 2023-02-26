import os
import string
import pyttsx3
engine = pyttsx3.init()
engine.setProperty("stripPunct",True)
engine.setProperty("rate", 100)
engine.setProperty("volume", 1.0)
# engine.setProperty("voice", engine.getProperty("voices")[0].id)
# engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Brian22')
# engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
input_file = "Selected Notes.txt"
output_file = "output.mp3"
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice.id)

# file = open(input_file, "r",encoding='utf-8')
file = open(input_file, "r",encoding='latin-1')
textlist = [] 
for line in file:
    word = line.split("\t")[0]
    letters = list(word) 
    explain = line.split("\t")[7]
    words =  (word +'. ')*3
    textlist.append(words)
    textlist.append(explain)
    # textlist.append(letters)
file.close

# for i,text in enumerate(textlist):
#     if i % 2 == 0:
#        engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
#     else:
#        engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
    # engine.say(text)

# engine.save_to_file(text, output_file)

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
engine.save_to_file(textlistlatin1, output_file)
engine.runAndWait()
