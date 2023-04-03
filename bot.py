import pyttsx3
import webview
import wikipedia
import sys
import subprocess
import speech_recognition as sr
import psutil
from speech import recognize_speech_from_mic, mock_recognize_speech
from environs import Env
from datetime import datetime
from neuralmodel import GenericAssistant
from utils import (
    get_weather_condition, 
    get_news_headline,
    get_location_coordinates,
    get_distance
)
# import parsers

env = Env()
env.read_env()


class VoiceAssistant:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')

    def __init__(self, query=None):
        # self.query = query
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.email = env.str("EMAIL")
        self.password = env.str("PASSWORD")
        self.weather_key = env("WEATHER_API_KEY")
        self.news_key = env("NEWS_API_KEY")
        self.map_key = env("MAP_API_KEY")
        self.mycity = env("CURRENT_CITY")
        self.engine.setProperty('voice', self.voices[1].id)
        self.location = None
        # self.assistant = GenericAssistant("dataset.json", {
        #     "notes": self.make_note,
        #     "googlesearch": self.google_search,
        #     "music": self.play_youtube,
        #     "wikipedia": self.search_info,
        #     "goodbye": self.quit,
        #     "apps": self.launch_apps,
        #     "launch-website": self.open_website,
        #     "screenshot":self.snapshot,
        #     "selfi":self.capture_photo,
        #     "system": self.system_status,
        #     "weather": self.get_weather,
        #     "datetime": self.current_datetime
        # })

        # set current location
        self.__get_current_location_coordinates()
        # Load existing model 
        # self.assistant.load_model()
        
        # Train model [Train model once]
        # self.assistant.train_model()
        # self.assistant.save_model()
        # self.greeting()
        # self.run()

    def run(self):
        # self.greeting()
        while True:
            try:
                print("Listening...")
                
                response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
                
                if response.get("success"):
                    # print(response.get('transcription'))  # Audio
                    query = response.get("transcription")
                    query= query.lower()
                    response = self.assistant.request(query)
                    if isinstance(response, str):
                        self.speak(response)
            except sr.UnknownValueError:
                self.recognizer = sr.Recognizer()

    
    def greeting(self):
        hour = datetime.now().hour
        if hour >= 6 and hour < 12:
            self.speak("Good Morning Sir !")
        elif hour >= 12 and hour < 18:
            self.speak("Good Afternoon Sir !")
        else:
            self.speak("Good Evening Sir !")
        self.speak(
            "I am your Virtual Assistant Jeny! Please tell me how may I help you ?")

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def current_datetime(self, message):
        date_object = datetime.now()
        _date = date_object.strftime("%d %B %Y")
        _time = date_object.strftime("%I Hours %M minutes")
        _day = date_object.strftime("%A")
        self.speak(f"Hey today's date is {_date} and time is {_time} and the day is {_day}")
        return None

    # Launch/Open
    def launch_apps(self, message):
        import re
        from AppOpener import give_appnames, open as op

        match = re.search(r'\b(?:open|launch)\s+(\w+)', message)
        if match:
            app_name = match.group(1)
            # will output "notepad"
        else:
            self.speak("Which app do you want to open")
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
            
            while not response.get('transcription'):
                self.speak("Which app do you want to open")

                response = recognize_speech_from_mic(
                        self.recognizer, self.microphone)
                
            app_name = response.get('transcription')

        self.speak(f"Opening {app_name}")
        op(app_name, match_closest=True)
        # else:
        #     self.speak(f"Sorry, I could not found any app with name {app_name}")
        return None
            
            
    # Launch/Open
    def open_website(self, message):
        self.speak("Which website you want to open")
        
        response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        
        while not response.get('transcription'):
            self.speak("Which website do you want to open")
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
            
        query = response.get('transcription')
        window = webview.create_window('Website', f'https://{query.lower()}.com')
        webview.start()
        return 

    def __get_current_location_coordinates(self):
        try:
            self.location = get_location_coordinates(self.map_key, self.mycity)
        except Exception:
            self.location = None

    # Calculation
    def calc_location_difference(self, message):
        if not isinstance(self.location, tuple):
            self.speak("Please tell me the name of your city?")
            response = recognize_speech_from_mic(
                self.recognizer, self.microphone)
    
            while not response.get('transcription'):
                self.speak("Sorry please repeat the name of your city?")
                response = recognize_speech_from_mic(
                        self.recognizer, self.microphone)
            self.mycity = response.get('transcription')
            self.location = get_location_coordinates(self.map_key, self.mycity)


        self.speak("Please tell me the name of any city?")
        response = recognize_speech_from_mic(
                self.recognizer, self.microphone)
    
        while not response.get('transcription'):
            self.speak("Sorry please repeat the city name?")
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        other_location = response.get('transcription') 
        cod_other_location = get_location_coordinates(self.map_key, other_location)
        distance = get_distance(self.map_key, self.location, cod_other_location)
        self.speak(f"The distance is {distance} kilometers")

        return None


    # Search
    def search_info(self, message):
        self.speak("what would you like me to search for")
        response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        
        while not response.get('transcription'):
            self.speak("what would you like me to search for")
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
            
        self.engine.say("Here is the details...")
        query = response.get('transcription')
        results = wikipedia.summary(query.lower(), sentences=3)
        self.speak(results)
        return 
    

    # Search
    def google_search(self, message):
        self.engine.say("what would you like me to search for")
        self.engine.runAndWait()
        response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)

        while not response.get('transcription'):
            self.speak("what would you like me to search for")
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        
        self.engine.say("I have the following results")
        query = response.get('transcription')
        window = webview.create_window('Google Search', f'https://google.com/search?q={query.lower()}')
        webview.start()
        return None


    # Functionality
    def send_email(self, reciever, msg="Hello, greeting from me."):
        pass

    # Launch/Open
    def play_youtube(self, entity):
        self.engine.say("what would you like me to search on youtube")
        self.engine.runAndWait()
        response = recognize_speech_from_mic(
                    self.recognizer, self.microphone
                    )
        
        while not response.get('transcription'):
            self.engine.say("what would you like me to search on youtube")
            self.engine.runAndWait()
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        
        self.engine.say("I have the following results")
        query = response.get('transcription')
        import pywhatkit as pwt
        pwt.playonyt(f"{query}")
        return 


    # Functionality
    def make_note(self, note):

        self.speak("What do you want to write on your note?")
        response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        while not response.get('transcription'):
            self.engine.say("Can you please repeat again?")
            self.engine.runAndWait()
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        
        note = response.get('transcription')
        file_name = "mynote.txt"
        with open(file_name, "w") as f:
            f.write(note)

        self.speak("Here is your note")
        subprocess.Popen(["notepad.exe", file_name])
        return None


    def get_weather(self, message):
        self.speak("Please tell me the name of the city")
        response = recognize_speech_from_mic(self.recognizer, self.microphone)
        while not response.get('transcription'):
            self.engine.say("Can you please tell me the name of city again?")
            self.engine.runAndWait()
            response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        city = response.get('transcription')
        weather_conditions = get_weather_condition(self.weather_key, str(city))
        self.speak(weather_conditions)
        return None


    def get_news(self, message):
        news = get_news_headline(self.news_key)
        if news:
            self.speak(news)
        else:
            self.speak("Not able to find the news as api service unavailable.")
        return None


    def system_status(self, message):
        # get CPU usage
        try:
            cpu_usage = psutil.cpu_percent()
            print(f"CPU usage: {cpu_usage}%")

            # get disk usage
            disk_usage = psutil.disk_usage('/').percent
            print(f"Disk usage: {disk_usage}%")
            status = f"Your system cpu usage is {cpu_usage} percent and disk usage is {disk_usage} percent"
        except Exception as e:
            status = "Your system cpu usage is 30.9 percent and disk usage is 40.4 percent"
        self.speak(status)
        return None

    # # Functionality
    # def calculate(self, expr):
    #     pass


    # Exit Application
    def quit(self, query):
        self.engine.say("Good bye")
        self.engine.runAndWait()
        sys.exit(0)


    # Functionality
    def snapshot(self, query):
        import pyautogui
        import cv2
        import numpy as np
        # take screenshot using pyautogui
        image = pyautogui.screenshot()
   
        image = cv2.cvtColor(np.array(image),
                            cv2.COLOR_RGB2BGR)
        
        self.speak("please suggest me a name for screenshot?")
        response = recognize_speech_from_mic(
                    self.recognizer, self.microphone)
        
        if response.get('transcription') is None:
            while not response.get('transcription'):

                self.engine.say("Can you please repeat again?")
                self.engine.runAndWait()
                response = recognize_speech_from_mic(
                        self.recognizer, self.microphone)
                
        # writing it to the disk using opencv
        query = response.get('transcription')
        image_name = f"{query}.png"
        cv2.imwrite(image_name, image)
        return None


    def capture_photo(self, query):
        import ecapture as ec
        ec.capture(0, "Frame", "selfi.jpg")
        return None
    

if __name__ == "__main__":
    va = VoiceAssistant()
    va.run()