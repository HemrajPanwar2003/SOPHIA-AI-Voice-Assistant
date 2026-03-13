from datetime import time

import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)

    except Exception as e:  # noqa: F841
        return ""

    return query.lower()


@eel.expose
def allCommands():

    query = takeCommand()
    print(query)

    if not query:
        return

    query = query.lower()

    if "open" in query:
        from engine.features import openCommand

        openCommand(query)

    elif "youtube" in query:
        from engine.features import PlayYoutube

        PlayYoutube(query)

    else:
        print("Command not recognized")


eel.ShowHood()
