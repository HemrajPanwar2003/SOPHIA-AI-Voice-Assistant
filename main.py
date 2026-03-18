import os
import eel
from engine.features import playAssistantSound
from engine.command import takeCommand

takeCommand


def start():
    eel.init("www")


playAssistantSound()


os.system('start chrome.exe --app="http://localhost:8000/index.html"')
eel.start("index.html", mode="chrome", host="localhost", block=True)
