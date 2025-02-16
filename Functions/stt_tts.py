import speech_recognition as sr
import pyttsx3

class STT:
    """Speech-to-Text (STT) System"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        """Listen from microphone and return recognized text"""
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ Recognized: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return ""
            except sr.RequestError:
                print("⚠️ STT Service Unavailable")
                return ""

class TTS:
    """Text-to-Speech (TTS) System"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Set speed
        self.engine.setProperty('volume', 1.0)  # Set volume

    def speak(self, text):
        """Convert text to speech and play it"""
        print(f"🔊 Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
