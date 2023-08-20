import os
import pyttsx3


async def absvr(text, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    engine = pyttsx3.init()
    engine.save_to_file(text, path)
    engine.runAndWait()
