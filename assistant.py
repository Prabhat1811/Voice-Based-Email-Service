import speech_recognition as sr
import pyttsx3


class Assistant:
    def __init__(self,name,speechRate):
        self._name = name
        self._speechRate = speechRate
        self.r = sr.Recognizer()
        self.command = None
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def get_recognized_audio(self):
        return self.command
    
    def set_recognized_audio(self, arg):
        self.command = arg

    def speak(self,text):
        engine = pyttsx3.init()
        engine. setProperty("rate", self._speechRate)
        engine.say(text)
        engine.runAndWait()

    def listen(self, text = ""):
        with sr.Microphone() as source:
            self.speak(text)
            # self.r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.r.listen(source, timeout = 3)
                return self.r.recognize_google(audio)
            except:
                # self.speak("I didn't hear anything")
                return ""
    
    def callback(self, recognizer, audio):
        try:
            # self.r.adjust_for_ambient_noise(source, duration=1)
            recognized = self.r.recognize_google(audio)
            self.command = recognized
            # print(self.command)
            return recognized
        except:
            self.command = ""
            return ""

    def listen_constantly(self):
        mic = sr.Microphone()
        stopper = self.r.listen_in_background(mic, self.callback)
        return stopper
