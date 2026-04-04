from datetime import time
import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    text = str(text)
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
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

    try:
        # 🔹 TEXT INPUT
        if message != 1:
            query = message.lower().strip()
            print(query)
            eel.senderText(query)

        # 🔹 VOICE INPUT (single run only)
        else:
            query = takeCommand()
            if not query:
                return
            query = query.lower().strip()
            print(query)
            eel.senderText(query)

        # ================= OPEN =================
        if "open" in query:
            from engine.features import openCommand

            openCommand(query)

        # ================= YOUTUBE =================
        elif "youtube" in query or "play" in query:
            from engine.features import PlayYoutube

            PlayYoutube(query)
            speak("Playing on YouTube")

        # ================= WHATSAPP =================
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp

            flag = ""

            contact_no, name = findContact(query)
            if contact_no != 0:
                if "send message" in query:
                    message = "message"
                    speak("what message to send")
                    query = takeCommand()
                elif "phone call" in query:
                    flag = "call"
                else:
                    flag = "video call"

                whatsApp(contact_no, query, flag, name)

        # ================= DEFAULT =================
        else:
            from engine.features import chatBot

            chatBot(query)
            eel.ShowHood()

    except Exception as e:
        print(f"⚠️ Error: {e}")
        speak("Something went wrong")
