from datetime import time
import os
from shlex import quote
import sqlite3
import struct
import subprocess
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

from engine.helper import extract_yt_term, remove_words

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


def findContact(query):
    from db import get_connection

    words_to_remove = [
        ASSISTANT_NAME,
        "make",
        "a",
        "to",
        "phone",
        "call",
        "send",
        "message",
        "whatsapp",
        "video",
    ]

    # Clean query
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()

        con, cursor = get_connection()

        cursor.execute(
            """
        SELECT name, mobile_no FROM contacts
        WHERE LOWER(name) LIKE ?
        """,
            ("%" + query + "%",),
        )

        results = cursor.fetchall()
        con.close()

        # ✅ Check if contact exists
        if not results:
            speak("Contact not found")
            return 0, 0

        name, mobile_number = results[0]

        mobile_number = str(mobile_number).replace(" ", "").replace("-", "")

        # ✅ Add country code if missing
        if not mobile_number.startswith("+91"):
            mobile_number = "+91" + mobile_number

        return mobile_number, name

    except Exception as e:
        print("Error:", e)
        speak("Error finding contact")
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    if flag == "message":
        target_tab = 12
        jarvis_message = f"Message sent to {name}"

    elif flag == "call":
        target_tab = 7
        message = ""
        jarvis_message = f"Calling {name}"

    else:
        target_tab = 6
        message = ""
        jarvis_message = f"Starting video call with {name}"

    # Encode message
    encoded_message = quote(message)

    # WhatsApp URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Open WhatsApp
    subprocess.run(f'start "" "{whatsapp_url}"', shell=True)

    # Wait for WhatsApp to load
    time.sleep(8)

    # Navigate using TAB
    for _ in range(target_tab):
        pyautogui.press("tab")

    # Press Enter
    pyautogui.press("enter")

    speak(jarvis_message)
