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
        # 🔹 Initialize Porcupine
        porcupine = pvporcupine.create(keywords=["krishna", "alexa"])

        # 🔹 Initialize PyAudio
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )
        # 🔹 Continuous Listening Loop
        while True:
            try:
                pcm = audio_stream.read(
                    porcupine.frame_length, exception_on_overflow=False
                )
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("🔥 Hotword detected!")

                    # 🔹 Trigger shortcut (Win + J)
                    autogui.keyDown("win")
                    autogui.press("j")
                    autogui.keyUp("win")

                    time.sleep(1)

            except Exception as e:
                print(f"⚠️ Audio read error: {e}")

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # 🔹 Always cleanup
        print("🧹 Cleaning up resources...")
        if audio_stream is not None:
            try:
                audio_stream.stop_stream()
            except Exception as e:
                print(f"Error stopping audio stream: {e}")
            try:
                audio_stream.close()
            except Exception as e:
                print(f"Error closing audio stream: {e}")
            except Exception as e:
                print(f"Error in cleanup: {e}")
                if paud is not None:
                    try:
                        paud.terminate()
                    except Exception as e:
                        print(f"Error terminating PyAudio: {e}")
        if porcupine is not None:
            try:
                porcupine.delete()
            except Exception as e:
                print(f"Error deleting Porcupine: {e}")
                print("✅ Cleanup complete")


def whatsApp(mobile_no, message, flag, name):

    if not mobile_no:
        speak("Invalid contact")
        return

    # 🔹 Decide action
    if flag == "message":
        target_tab = 12
        krishna_message = f"Message sent successfully to {name}"

    elif flag == "call":
        target_tab = 7
        message = ""
        krishna_message = f"Calling {name}"

    elif flag == "video":
        target_tab = 6
        message = ""
        krishna_message = f"Starting video call with {name}"

    else:
        speak("Invalid action")
        return

    # 🔹 Encode message
    encoded_message = quote(message)

    # 🔹 WhatsApp URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # 🔹 Open WhatsApp
    subprocess.run(f'start "" "{whatsapp_url}"', shell=True)

    time.sleep(5)  # wait for WhatsApp to open

    # 🔹 Navigate UI
    for _ in range(target_tab):
        autogui.press("tab")
        time.sleep(0.1)

    autogui.press("enter")

    speak(krishna_message)
