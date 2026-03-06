from playsound import playsound
import eel


# Sound function
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound 123.mp3"
    playsound(music_dir)


# Click Sound Function
@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)
