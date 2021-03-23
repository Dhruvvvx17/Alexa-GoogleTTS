# source code for JARVIS AI

# import statements
import os
import random
import pyjokes
import datetime
import wikipedia
import pywhatkit
import playsound
import webbrowser
from gtts import gTTS
import speech_recognition as sr

from basics import *

# recognizer object - capture input audio
recognizer = sr.Recognizer()


def record_audio(ask = False):
    '''
    Function to record audio from microphone and convert to speech using google speech recognition API

    Returns:
    String - Input voice data as text
    '''
    # initialize microphone as input source
    with sr.Microphone() as source:
        if(ask):
            speak(ask)
        print("Listening...")
        audio = recognizer.listen(source)
        voice_data = ''
        # convert speech to text using google speech recognition API
        try:
            voice_data = recognizer.recognize_google(audio)
        # handle exceptions
        except sr.UnknownValueError:
            speak(f'{failed_to_understand}')
        except sr.RequestError:
            speak(f'{service_down}')
    
        return voice_data


def respond(voice_data):
    '''
    Function to respond to the voice data query based on the response logic

    Returns:

    '''
    if 'what is your name' in voice_data:
        speak(f"{self_name}")

    elif ('what time is it' in voice_data) or ('what is the time' in voice_data):
        current_time = datetime.datetime.now()
        if(current_time.hour>12):
            hour = current_time.hour - 12
            meridian = "PM"
        else:
            hour = current_time.hour
            meridian = "AM"
        speak(f"The time is: {hour} {current_time.minute} {meridian}")

    elif 'search' in voice_data:
        search = record_audio(f'{search_request}')
        url = f'https://google.com/search?q={search}'
        webbrowser.get().open(url)
        speak(f"{found_text_web}'{search}'")

    elif 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = f'https://google.com/maps/place/{location}/&amp;'
        webbrowser.get().open(url)
        speak(f"{found_text_maps}'{location}'")

    elif ('play a song' in voice_data) or ('play music' in voice_data) or ('song' in voice_data):
        song = record_audio("What song do you want to play?")
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
        exit()

    elif ('info' in voice_data) or ('information' in voice_data):
        info_on = record_audio('What do you want information on?')
        try:
            res = wikipedia.summary(info_on, 2)
            speak(f"This is what I got on {info_on}: {res}")
        except:
            speak(f"{no_wiki_info} {info_on}")

    elif ('joke' in voice_data):
        speak(f"Here is a joke for you\n{pyjokes.get_joke()}")

    elif 'exit' in voice_data:
        speak(f'{random.choice(exit_text)}')
        exit()

    else:
        speak(f'{voice_data}')



def speak(audio_string):
    '''
    Function to convert text to audo using gTTS
    '''
    print(audio_string)
    tts = gTTS(text=audio_string, lang="en-us")
    audio_file = "./AUDIO/audio-temp.mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)


if __name__ == "__main__":

    greeting = random.choice(greetings)
    speak(f"{greeting}! {help_text}")

    while(True):
        voice_data = record_audio()
        respond(voice_data)