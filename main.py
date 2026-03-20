import eel
from engine.features import playAssistantSound
from engine.command import takeCommand

takeCommand
playAssistantSound()


def start():
    eel.init("www")
    eel.start("index.html", mode="chrome", host="localhost", port=8000)
