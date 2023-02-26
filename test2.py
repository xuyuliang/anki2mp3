import os
import sys
import codecs
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3,SYLT, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC

# Read the ID3 tag or create one if not present
audio = "test3.mp3"
try: 
    tags = ID3(audio)
except ID3NoHeaderError:
    print("Adding ID3 header")
    tags = ID3()

# tags["TIT2"] = TIT2(encoding=3, text=u'title')
# tags["TALB"] = TALB(encoding=3, text=u'mutagen Album Name')
# tags["TPE2"] = TPE2(encoding=3, text=u'mutagen Band')
# tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
# tags["TPE1"] = TPE1(encoding=3, text=u'mutagen Artist')
# tags["TCOM"] = TCOM(encoding=3, text=u'mutagen Composer')
# tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
# tags["TDRC"] = TDRC(encoding=3, text=u'2010')
# Create a new lyrics tag
# lyrics = SYLT(encoding=3, lang=u'eng', format=2, type=1, desc=u'', text=u'This is the synchronized lyrics.')
# lyrics.add_time_stamp(0, TIME_STAMP_FORMAT.MILLISECONDS, '00:00.000')
# lyrics = USLT(encoding=3, lang=u'eng', desc=u'', text=u'This is the lyrics.')
sync_lyrics = [
    ("first line lyric",0),
    ("second line ",500),
    ("3 line",1000)
]

# Add the lyrics tag to the MP3 file
tags.setall("SYLT", [SYLT(encoding=3, lang=u'chi', format=2, type=1, text=sync_lyrics)])
tags.save(v2_version=3)