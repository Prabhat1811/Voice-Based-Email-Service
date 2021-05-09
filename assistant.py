import speech_recognition as sr
import pyttsx3


class Assistant:
    def __init__(self, name, speechRate = 135, voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0", threshold = 300):
        self._name = name
        self._speechRate = speechRate
        self.voice = voice
        self.r = sr.Recognizer()
        self.r.energy_threshold = threshold
        self.r.dynamic_energy_threshold = True
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
        try:
            engine = pyttsx3.init()
            engine.setProperty("voice", self.voice)
            engine. setProperty("rate", self._speechRate)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            return e

    def listen(self, text = ""):
        try:
            with sr.Microphone() as source:
                self.speak(text)
                # self.r.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = self.r.listen(source, timeout = 3)
                    return self.r.recognize_google(audio)
                except:
                    # self.speak("I didn't hear anything")
                    return ""
        except Exception as e:
            return e
    
    def callback(self, recognizer, audio):
        try:
            # self.r.adjust_for_ambient_noise(source, duration=1)
            recognized = self.r.recognize_google(audio)
            self.command = recognized
            # print(self.command)
            return recognized
        except Exception as e:
            self.command = ""
            return ""

    def listen_constantly(self):
        mic = sr.Microphone()
        stopper = self.r.listen_in_background(mic, self.callback)
        return stopper

# a = Assistant('name',150)

# print(a.listen('speak'))

# s = a.listen_constantly()

# if a.callback() == "name":
#     # print(True)

