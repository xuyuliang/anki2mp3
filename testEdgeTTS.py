import asyncio
import edge_tts

TEXT = "Hello World! 你真好"
VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "test.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

def do_edgetts(text,outputfile):
    
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()

if __name__ == "__main__":
    do_edgetts(TEXT,OUTPUT_FILE)