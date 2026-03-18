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

    except Exception as e:
        print(f"Speech error: {e}")
        eel.DisplayMessage(f"Speech error: {str(e)}")

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

    elif "youtube" in query or "play" in query:
        try:
            from engine.features import PlayYoutube

            PlayYoutube(query)
            speak("Playing on YouTube")
        except ImportError:
            speak("YouTube module not found")

    else:
        speak("Sorry, I didn't understand that command")

    eel.ShowHood()
