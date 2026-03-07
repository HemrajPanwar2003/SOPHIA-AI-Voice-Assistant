import os
import eel

from engine.features import playAssistantSound

playAssistantSound()

os.system('start chrome.exe --app="http://localhost:8000/index.html"')

eel.init("www")

eel.start("index.html", mode="chrome", host="localhost", block=True)
