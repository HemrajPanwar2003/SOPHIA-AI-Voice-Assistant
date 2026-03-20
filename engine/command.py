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
    try:
        query = takeCommand()
        print(query)
    except Exception as e:
        print(f"Error in allCommands: {e}")
        eel.DisplayMessage(f"Error: {str(e)}")
        return

    if not query:
        return

    query = query.lower()

    try:
        # 🔹 OPEN COMMAND
        if "open" in query:
            from engine.features import openCommand

            openCommand(query)

        # 🔹 YOUTUBE
        elif "youtube" in query or "play" in query:
            from engine.features import PlayYoutube

            PlayYoutube(query)
            speak("Playing on YouTube")

        # 🔹 WHATSAPP (MESSAGE / CALL / VIDEO)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp

            contact_no, name = findContact(query)

            if contact_no != 0:
                # MESSAGE
                if "send message" in query:
                    speak("What message should I send?")
                    user_message = takeCommand()

                    if not user_message:
                        speak("Message not received")
                        return

                    whatsApp(contact_no, user_message, "message", name)

                # CALL
                elif "phone call" in query:
                    whatsApp(contact_no, "", "call", name)

                # VIDEO CALL
                else:
                    whatsApp(contact_no, "", "video", name)

        # 🔹 UNKNOWN COMMAND
        else:
            speak("Sorry, I didn't understand that command")
            eel.ShowHood()

    except ImportError as e:
        print(f"Import Error: {e}")
        speak("Required module not found")

    except Exception as e:
        print(f"Error: {e}")
        speak("Something went wrong")
        eel.ShowHood()
