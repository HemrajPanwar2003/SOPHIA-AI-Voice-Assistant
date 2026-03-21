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

    if "open" in query:
        from engine.features import openCommand

        openCommand(query)

    elif "youtube" in query or "play" in query:
        try:
            from engine.features import PlayYoutube

            PlayYoutube(query)
            speak("Playing on YouTube")
        except Exception as e:
            print(f"Error playing YouTube: {e}")
            speak("Could not play on YouTube")

    elif any(
        phrase in query.lower()
        for phrase in ["send message", "phone call", "video call"]
    ):
        try:
            from engine.features import findContact, whatsApp

            contact_no, name = findContact(query)

            if contact_no == 0:
                speak("Sorry, I couldn't find that contact in your phone.")
            else:
                if "send message" in query.lower():
                    speak("What message would you like to send?")
                    message_content = takeCommand().strip()
                    if message_content:
                        whatsApp(contact_no, message_content, "message", name)
                        speak(f"Message sent to {name}")
                    else:
                        speak("No message provided")

                elif "phone call" in query.lower():
                    speak(f"Calling {name}...")
                    whatsApp(contact_no, query, "call", name)

                elif "video call" in query.lower():
                    speak(f"Starting video call with {name}...")
                    whatsApp(contact_no, query, "video call", name)

        except ImportError:
            speak("Required modules not found")
        except Exception as e:
            speak("Sorry, there was an error processing your request")
            print(f"Error: {e}")

    eel.ShowHood()
