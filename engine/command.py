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
def allCommands(message=1):

    if message == 1:
        query = takeCommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "open" in query:
            from engine.features import openCommand

            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube

            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage

            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takeCommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("what message to send")
                        message = takeCommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = "message"
                        speak("what message to send")
                        query = takeCommand()

                    elif "phone call" in query:
                        message = "call"
                    else:
                        message = "video call"

                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import geminai

            geminai(query)
    except Exception as e:
        print(f"Error: {e}")
    eel.ShowHood()
