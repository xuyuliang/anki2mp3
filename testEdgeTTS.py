import asyncio
import edge_tts

VOICE = "en-GB-SoniaNeural"

async def communicate_async(text, outputfile):
    """异步函数用于文本到语音的转换"""
    communicate = edge_tts.Communicate(text, VOICE,rate="-30%")
    await communicate.save(outputfile)

def process_text(text, outputfile):
    """处理文本到语音的转换"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(communicate_async(text, outputfile))
    loop.close()

if __name__ == "__main__":
    myTEXT = ["Hello", "World", "pantry", "plane"]
    myOUTPUT_FILE = "test.mp3"
    for i, text in enumerate(myTEXT, start=1):
        process_text(text, str(i) + myOUTPUT_FILE)