import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import time
import pygame
import numpy as np
import sys
import os
import threading

# ====================== CONFIGURATION ======================
WAKE_WORDS = ["wake up", "jarvis", "hey jarvis", "computer", "hey computer"]
ENERGY_THRESHOLD = 300 
PAUSE_THRESHOLD = 0.8
COMMAND_TIMEOUT = 10
WAKE_WORD_TIMEOUT = 3 
MAX_RETRIES = 3

# ====================== INITIALIZATION ======================
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
except Exception as e:
    print(f"TTS Initialization Error: {e}")
    sys.exit(1)

def print_and_speak(text):
    if not text:
        return
    print(text)
    clean_text = text.replace("====", "").replace("✅", "").replace("🤖", "").replace("🚀", "")
    try:
        engine.say(clean_text)
        engine.runAndWait()
        time.sleep(0.1)
    except Exception as e:
        print(f"Speech error: {e}")

try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
except Exception as e:
    print(f"Audio system error: {e}")

class AssistantState:
    is_assistant_active = False

# ====================== AUDIO UTILITIES ======================
def generate_tone(frequency, duration_ms, volume=0.3):
    sample_rate = 44100
    samples = int(duration_ms * sample_rate / 1000)
    t = np.linspace(0, duration_ms/1000, samples, False)
    tone = np.sin(2 * np.pi * frequency * t) * 32767 * volume
    stereo_tone = np.column_stack((tone.astype(np.int16), tone.astype(np.int16)))
    return stereo_tone

class SoundEffects:
    def __init__(self):
        self.activate = self._create_chime(600, 900)
        self.deactivate = self._create_chime(900, 600)
    
    def _create_chime(self, freq1, freq2):
        try:
            t1 = generate_tone(freq1, 150)
            t2 = generate_tone(freq2, 150)
            return pygame.sndarray.make_sound(np.vstack((t1, t2)))
        except: return None

sounds = SoundEffects()

def play_sound(sound_type):
    if sounds:
        if sound_type == "activate" and sounds.activate:
            sounds.activate.play()
        elif sound_type == "deactivate" and sounds.deactivate:
            sounds.deactivate.play()

# ====================== CORE FUNCTIONS ======================
def calibrate_microphone(recognizer, source):
    print_and_speak("Starting microphone calibration. Please remain quiet...")
    try:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        recognizer.dynamic_energy_threshold = True 
        print_and_speak("Calibration complete.")
        return True
    except Exception as e:
        print_and_speak("Calibration failed.")
        return False

def listen_for_wake_word(recognizer, source):
    try:
        audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
        text = recognizer.recognize_google(audio).lower()
        if any(word in text for word in WAKE_WORDS):
            play_sound("activate")
            print_and_speak("Wake word detected. I am listening.")
            AssistantState.is_assistant_active = True
            return True
    except:
        pass
    return False

def take_command(recognizer, source):
    """Refined listening function that catches silent/inaudible errors."""
    print_and_speak("Listening for your command...")
    try:
        audio = recognizer.listen(source, timeout=COMMAND_TIMEOUT, phrase_time_limit=COMMAND_TIMEOUT)
        query = recognizer.recognize_google(audio).lower()
        print_and_speak(f"You said: {query}")
        return query
    except sr.WaitTimeoutError:
        print_and_speak("I didn't hear anything. Time out.")
        return None
    except sr.UnknownValueError:
        print_and_speak("Audio was not clear or audible.")
        return None
    except Exception as e:
        print(f"Unexpected error in listening: {e}")
        return None

def process_command(query):
    if not query: return

    if 'wikipedia' in query or 'search for' in query:
        topic = query.replace("wikipedia", "").replace("search for", "").strip()
        if topic:
            print_and_speak(f"Searching Wikipedia for {topic}...")
            try:
                results = wikipedia.summary(topic, sentences=2)
                print_and_speak(f"According to Wikipedia: {results}")
            except Exception:
                print_and_speak("I couldn't find details on that topic.")
        else:
            print_and_speak("What should I search for?")

    elif 'open youtube' in query:
        print_and_speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
        
    elif 'open google' in query or 'open chrome' in query:
        print_and_speak("Opening Google Chrome.")
        webbrowser.open("https://google.com")
        
    elif 'time' in query:
        print_and_speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")
        
    elif 'joke' in query:
        print_and_speak(pyjokes.get_joke())

    elif any(word in query for word in ['exit', 'quit', 'shutdown']):
        play_sound("deactivate")
        print_and_speak("Goodbye.")
        sys.exit(0)
    
    elif any(word in query for word in ['sleep', 'stop listening']):
        print_and_speak("Standing by.")
        play_sound("deactivate")
        AssistantState.is_assistant_active = False

# ====================== MAIN EXECUTION ======================
def main():
    print_and_speak("JARVIS SYSTEM INITIALIZING")
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            calibrate_microphone(recognizer, source)
            print_and_speak("System online. Say 'wake up' to start.")

            while True:
                if not AssistantState.is_assistant_active:
                    listen_for_wake_word(recognizer, source)
                else:
                    query = take_command(recognizer, source)
                    if query:
                        process_command(query)
                    
                    # Always return to standby after a command attempt
                    if AssistantState.is_assistant_active:
                        print_and_speak("Returning to standby.")
                        play_sound("deactivate")
                        AssistantState.is_assistant_active = False

    except KeyboardInterrupt:
        print_and_speak("Manual exit. Goodbye.")
    except Exception as e:
        print(f"Fatal System Error: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    main()