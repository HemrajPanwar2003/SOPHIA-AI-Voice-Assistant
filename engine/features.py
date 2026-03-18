import os
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

con = sqlite3.connect("sophia.db")
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


def extract_yt_term(command):
    """Improved regex patterns for YouTube search extraction"""
    command = str(command).lower()

    # Multiple patterns for different ways users might speak
    patterns = [
        r"play\s+(.+?)(?:\s+on\s+youtube|\s+on\s+yt)?$",
        r"(?:youtube|yt)\s+(.+?)$",
        r"play\s+(.+?)(?=\s|$)",
        r"open\s+youtube\s+(.+?)$",
    ]

    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            term = match.group(1).strip()
            # Clean up the term
            term = re.sub(r"(music|song|video)\s+", "", term, flags=re.IGNORECASE)
            return term if len(term) > 1 else None

    # Fallback: everything after "play"
    if "play" in command:
        return command.split("play")[-1].strip()

    return None
