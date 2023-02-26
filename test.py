import pyttsx3
import datetime
from pydub import AudioSegment
import gtts
import eyed3
from eyed3.id3 import Tag 
# from playsound import playsound
text = 'apple cat british english vituperation fracas unguent'
text = "'pɜrs(ə)nɪdʒ"
tts = gtts.gTTS(text,lang="en")
tts.save("hello.mp3")

quit()

# the engine
engine = pyttsx3.init()
# engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Brian22')
# engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Amy22')
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0')
engine.setProperty("rate", 150)
# engine.say('vituperation')
engine.say("'pɜrs(ə)nɪdʒ")
# engine.save_to_file(text, 'test2.wav')

engine.runAndWait()
quit()
# load the mp3 as an audio
# audio = AudioSegment.from_file("test.mp3")
# audio = AudioSegment.from_file("./temp/1.mp3")
# print(audio.duration_seconds)

# t = datetime.datetime.now()
# print(str(t).split('.')[0].replace(' ','日').replace(':','-'))
AudioSegment.from_wav("test2.wav").export("test3.mp3", format="mp3")
quit()
mp3file = eyed3.load('test3.mp3')
if not mp3file.tag:
  mp3file.initTag(version=(2, 3, 0))
mp3file.tag.title =u'paul xu'
mp3file.tag.artist=u'paul xu'
mp3file.tag.album=u'paul xu'
image_data = open('封面.jpg',"rb").read()
mp3file.tag.images.set(3, image_data, 'image/jpeg', u'Cover')
# mp3file.tag.lyrics.set(u'哈哈这是中文 and english')
mp3file.tag.lyrics.set(text)
# mp3file.tag.lyrics.set(text)
# mp3file.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION,encoding='utf-8')
# mp3file.tag.save()
# mp3file.tag.save(version=(2, 3, 0))
t=Tag()
t.lyrics.set("new lyrics by me aaa")
t.save("test3.mp3")
print(mp3file.tag.lyrics[0].text)
print(mp3file.tag[0].text)


