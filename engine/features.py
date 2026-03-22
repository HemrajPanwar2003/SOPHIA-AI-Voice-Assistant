from datetime import time
import os
import sqlite3
import struct
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import urllib
from engine.command import speak, takeCommand
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

from engine.helper import extract_yt_term
from hugchat import hugchat

con = sqlite3.connect("Krishna.db")
cursor = con.cursor()


# Sound function
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound 123.mp3"
    playsound(music_dir)


# Click Sound Function
@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute(
                "SELECT path FROM sys_command WHERE name IN (?)", (app_name,)
            )
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    "SELECT url FROM web_command WHERE name IN (?)", (app_name,)
                )
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening " + query)
                    try:
                        os.system("start " + query)
                    except sqlite3.Error:
                        speak("not found")
        except ValueError:
            speak("some thing went wrong")
        finally:
            cursor.close()


def PlayYoutube(query):
    try:
        search_term = extract_yt_term(query)
        if not search_term:
            speak("No search term found for YouTube")
            return False

        speak(f"Playing {search_term} on YouTube")
        eel.DisplayMessage(f"🎵 Playing: {search_term}")

        # Use pywhatkit to play on YouTube
        kit.playonyt(search_term)
        return True

    except Exception as e:
        speak("Could not play on YouTube")
        print(f"❌ YouTube error: {e}")
        eel.DisplayMessage(f"❌ YouTube error: {str(e)}")
        return False


def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # pre trained keywords
        porcupine = pvporcupine.create(keywords=["krishna", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # processing keyword comes from mic
            keyword_index = porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index >= 0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui

                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except:  # noqa: E722
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# 🔍 FIND CONTACT
def findContact(query):
    words_to_remove = [
        "send",
        "message",
        "make",
        "call",
        "phone",
        "video",
        "to",
        "on",
        "whatsapp",
    ]

    query = query.lower()

    for word in words_to_remove:
        query = query.replace(word, "")

    query = query.strip()

    try:
        cursor.execute(
            "SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?",
            ("%" + query + "%",),
        )
        result = cursor.fetchone()

        if result:
            name, number = result
            return number, name

        else:
            return 0, 0

    except Exception as e:
        print("Database Error:", e)
        return 0, 0


# 📲 WHATSAPP FUNCTION
def whatsApp(contact_no, message, flag, name):
    try:
        encoded_message = urllib.parse.quote(message)

        if flag == "message":
            speak(f"Sending message to {name}")
            url = f"https:whatsapp.com//wa.me/{contact_no}?text={encoded_message}"
            webbrowser.open(url)

        elif flag == "call":
            speak(f"Calling {name}")
            url = f"https:whatsapp.com//wa.me/{contact_no}"
            webbrowser.open(url)

        elif flag == "video call":
            speak(f"Starting video call with {name}")
            url = f"https:whatsapp.com//wa.me/{contact_no}"
            webbrowser.open(url)

        else:
            speak("Invalid action")

    except Exception as e:
        print("WhatsApp Error:", e)
        speak("Something went wrong")


# 🎯 MAIN HANDLER FUNCTION
def handleCommunication(query):
    contact_no, name = findContact(query)

    if contact_no != 0:
        flag = None
        message_text = ""

        # 📩 MESSAGE
        if "send message" in query:
            flag = "message"

            # Try extracting message directly
            message_text = query.replace("send message", "").strip()

            if not message_text:
                speak("What message should I send?")
                message_text = takeCommand()

            if not message_text:
                speak("Message not received")
                return

        # 📞 CALL
        elif "phone call" in query:
            flag = "call"

        # 🎥 VIDEO CALL
        elif "video call" in query:
            flag = "video call"

        # 🚀 EXECUTE
        whatsApp(contact_no, message_text, flag, name)

    else:
        speak("Contact not found")

    # chat bot


def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
