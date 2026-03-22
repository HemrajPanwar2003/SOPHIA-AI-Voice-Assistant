from asyncio import subprocess
from datetime import time
from email.quoprimime import quote
import os
import sqlite3
import struct
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui as autogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

from engine.helper import extract_yt_term

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
        print("🎤 Starting hotword detection...")

        porcupine = pvporcupine.create(keywords=["krishna", "alexa"])

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        last_trigger_time = 0

        while True:
            pcm = audio_stream.read(
                porcupine.frame_length,
                exception_on_overflow=False,
            )
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                current_time = time.time()

                # 🔹 Cooldown (1.5 sec)
                if current_time - last_trigger_time > 1.5:
                    print("🔥 Hotword detected!")

                    autogui.keyDown("win")
                    autogui.press("j")
                    autogui.keyUp("win")

                    last_trigger_time = current_time

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        print("🧹 Cleaning up...")

        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()

        if paud:
            paud.terminate()

        if porcupine:
            porcupine.delete()

        print("✅ Cleanup done")


def whatsApp(mobile_no, message, flag, name):

    if not mobile_no:
        speak("Invalid contact")
        return

    if flag == "message":
        krishna_message = f"Message sent to {name}"
    elif flag == "call":
        message = ""
        krishna_message = f"Calling {name}"
    elif flag == "video":
        message = ""
        krishna_message = f"Starting video call with {name}"
    else:
        speak("Invalid action")
        return

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Open WhatsApp
    subprocess.Popen(f'start "" "{whatsapp_url}"', shell=True)

    # 🔹 Smart wait (instead of fixed 7 sec)
    time.sleep(5)

    if flag == "message":
        autogui.press("enter")

    speak(krishna_message)
