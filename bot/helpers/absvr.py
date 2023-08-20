import os
import pyttsx3


async def absvr(text, path, rate=125, volume=1.0, i=1):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[i].id)
    engine.save_to_file(text, path)
    engine.runAndWait()
