import speech_recognition as sr
import pyttsx3
import threading
import time

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("Available voices:")
for voice in voices:
    print(f"  - {voice.name}")

# Find best male voice
male_voice_id = None
for voice in voices:
    if 'david' in voice.name.lower():
        male_voice_id = voice.id
        print(f"Selected: {voice.name}")
        break
    elif male_voice_id is None:
        male_voice_id = voice.id

# Configure for SOFT MALE VOICE
engine.setProperty('voice', male_voice_id)
engine.setProperty('rate', 130)
engine.setProperty('volume', 0.7)

print(f"Voice ready!")

def speak(text, lang=None):
    """Speak the given text - always works"""
    if not text:
        return
    
    try:
        # Stop any previous speech
        engine.stop()
        
        # Set properties again (in case they changed)
        engine.setProperty('voice', male_voice_id)
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 0.7)
        
        # Speak directly (not in thread to ensure it works)
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"Speak error: {e}")
        # Try again with new engine
        try:
            engine2 = pyttsx3.init()
            engine2.setProperty('voice', male_voice_id)
            engine2.setProperty('rate', 130)
            engine2.setProperty('volume', 0.7)
            engine2.say(text)
            engine2.runAndWait()
            engine2.stop()
        except Exception as e2:
            print(f"Retry failed: {e2}")

def listen():
    """Listen to user's voice"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)
            
            # Try English
            try:
                text = recognizer.recognize_google(audio, language="en-IN")
                print(f"You said: {text}")
                return text.lower()
            except:
                pass
            
            # Try Hindi
            try:
                text = recognizer.recognize_google(audio, language="hi-IN")
                print(f"You said: {text}")
                return text.lower()
            except:
                return "Sorry, I didn't catch that."
                
        except Exception as e:
            print(f"Listen error: {e}")
            return "Sorry, I didn't catch that."

if __name__ == "__main__":
    print("Testing voice...")
    speak("Hello Aafuu! I am Bruno. How can I help you?")