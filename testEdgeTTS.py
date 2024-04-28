import asyncio
import edge_tts

# VOICE = "en-GB-RyanNeural"
VOICE = "zh-CN-XiaoxiaoNeural" #靡靡之音
# VOICE = "zh-TW-HsiaoChenNeural" #台湾女声
# VOICE = "zh-CN-XiaoyiNeural" #萌呆小朋友
# VOICE = "zh-CN-YunjianNeural" #男播音员

async def communicate_async(text, outputfile):
    """异步函数用于文本到语音的转换"""
    # communicate = edge_tts.Communicate(text, VOICE,rate="-20%")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(outputfile)

def process_text(text, outputfile):
    """处理文本到语音的转换"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(communicate_async(text, outputfile))
    loop.close()

if __name__ == "__main__":
    # myTEXT = ["Hello", "World", "pantry", "nephritis"]
    myTEXT = ["“重庆要以敢为人先的勇气，全面深化改革，扩大高水平对外开放。坚持和落实‘两个毫不动摇’，一手抓深化国企改革、培育一批核心竞争力强的国有企业，一手抓促进民营经济发展壮大、激发各类经营主体活力。积极融入全国统一大市场建设，主动融入和服务国家重大战略，在推动共建‘一带一路’、长江经济带、西部陆海新通道联动发展中发挥更大作用。主动对接高标准国际经贸规则，营造市场化法治化国际化一流营商环境。”习近平总书记的重要讲话在巴渝大地久久回响，振奋人心、催人奋进。"]
    myOUTPUT_FILE = "test.mp3"
    for i, text in enumerate(myTEXT, start=1):
        process_text(text, str(i) + myOUTPUT_FILE)