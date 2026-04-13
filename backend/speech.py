import speech_recognition as sr
import pyttsx3
from langdetect import detect

engine = pyttsx3.init()

# speed
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')

# Find Hindi and English voices automatically
hindi_voice = None
english_voice = None

for voice in voices:

    name = voice.name.lower()

    if "heera" in name or "hindi" in name or "india" in name:
        hindi_voice = voice.id

    if "zira" in name or "david" in name or "english" in name:
        english_voice = voice.id


# fallback
if english_voice is None:
    english_voice = voices[0].id

if hindi_voice is None:
    hindi_voice = voices[0].id


def speak(text):

    try:

        lang = detect(text)

        if lang == "hi":
            engine.setProperty('voice', hindi_voice)
        else:
            engine.setProperty('voice', english_voice)

    except:
        engine.setProperty('voice', english_voice)

    engine.say(text)
    engine.runAndWait()



def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)

        try:

            text = r.recognize_google(audio, language="hi-IN")
            print("User:", text)
            return text

        except:

            try:

                text = r.recognize_google(audio, language="en-IN")
                print("User:", text)
                return text

            except:

                return "Sorry, I didn't catch that."
