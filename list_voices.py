import pyttsx3

engine = pyttsx3.init()
engine.setProperty("stripPunct",True)
engine.setProperty("rate", 100)
engine.setProperty("volume", 1.2)
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id)
