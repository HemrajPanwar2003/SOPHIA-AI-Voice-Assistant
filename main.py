import os
import eel
from engine.features import playAssistantSound
from engine.command import takeCommand

eel.init("www")

playAssistantSound()
takeCommand()

os.system('start chrome.exe --app="http://localhost:8000/index.html"')
eel.start("index.html", mode="chrome", host="localhost", block=True)
