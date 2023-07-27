import speech_recognition as sr
import re

gameon = True
mappings = {
    "for the empress": "soviet.wav",
    "take ten": "ouch2.wav",
    "knocks out": "explosion.wav",
    "knocked down": "oof.wav",
    "you are stationary": "frozen.wav",
    "take fifteen": "ouch.wav",
    "critical stationary": "zap.wav",
    "thunderclap": "days_of_thunder_soundtrack.wav",
    "take twenty": "hahaha.wav",
    "he's dead": "graveyard.wav",
    "i need more": "shazbot.wav"
}

def stop():
    global gameon 
    gameon = False
    
def listenForPhrase(recognizer, mic):
    with mic as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    return audio

def prepare_recognizer(recognizer, mic):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

def playSound(sound):
    print("playing " + sound)

def checkMappings(transcriptions, mappings):
    if "alternative" not in transcriptions:
        return
    for transcriptDict in transcriptions["alternative"]:
        if "transcript" not in transcriptDict:
            continue
        for mapping in list(mappings.keys()):
            match = re.search(mapping, transcriptDict['transcript'],re.IGNORECASE)
            if match != None:
                playSound(mappings[mapping])

def start():
    global gameon
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    prepare_recognizer(recognizer,mic)
    while gameon == True:
        try:
            audio = listenForPhrase(recognizer, mic)
            transcriptions = recognizer.recognize_google(audio, show_all=True)
            checkMappings(transcriptions, mappings)
            print(transcriptions)
        except sr.RequestError as e:
            print(e)
            stop()

start()