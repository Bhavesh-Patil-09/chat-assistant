import tkinter as tk
import speech_recognition as sr
import pyttsx3
from neuralmodel import GenericAssistant
from PIL import ImageTk, Image
from bot import VoiceAssistant


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Assistant")
        self.master.geometry("675x450")

        # create background image
        self.background_image = Image.open("background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.master, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # create chat text box
        self.chat_textbox = tk.Text(self.master, height=10, width=30)
        self.chat_textbox.place(relx=0.5, rely=0.5, anchor='center')

        # # create chat input box
        # self.chat_input = tk.Entry(self.master, width=30)
        # self.chat_input.place(relx=0.5, rely=0.8, anchor='center')
        # self.chat_input.bind("<Return>", self.send_message)

        # create voice assistant
        self.voice_assistant = VoiceAssistant()
        mappings = {
            "notes": self.voice_assistant.make_note,
            "googlesearch": self.voice_assistant.google_search,
            "music": self.voice_assistant.play_youtube,
            "wikipedia": self.voice_assistant.search_info,
            "goodbye": self.voice_assistant.quit,
            "apps": self.voice_assistant.launch_apps,
            "launch-website": self.voice_assistant.open_website,
            "news":self.voice_assistant.get_news,
            "screenshot":self.voice_assistant.snapshot,
            "selfi":self.voice_assistant.capture_photo,
            "system": self.voice_assistant.system_status,
            "weather": self.voice_assistant.get_weather,
            "datetime": self.voice_assistant.current_datetime,
            "locationdistance": self.voice_assistant.calc_location_difference,
            "email": self.voice_assistant.send_email
            }

        # create ML model
        self.mymodel = GenericAssistant('dataset.json', mappings)
        self.mymodel.load_model()
        # self.mymodel.train_model()
        # self.mymodel.save_model()
        
        # greet user
        self.display_message("Hi,Click below voice button to start conversation?")
        
        # create speech recognition object
        self.recognizer = sr.Recognizer()

    # def send_message(self, event):
    #     message = self.chat_input.get()
    #     self.chat_input.delete(0, tk.END)
    #     self.display_message("You: " + message)
    #     # TODO: process user message and generate a response
    #     response = "I'm sorry, I don't know how to respond to that."
    #     self.display_message("Voice Assistant: " + response)
    #     self.voice_assistant.speak(response)

    def display_message(self, message):
        self.chat_textbox.insert(tk.END, message + "\n")

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            # self.display_message("Voice Assistant: Listening...")
            message = self.recognizer.recognize_google(audio)
            self.display_message("You: " + message)
            # TODO: process user message and generate a response
            response = self.mymodel.request(message)
            if response is not None:
                self.voice_assistant.speak(response)
                self.display_message("Voice Assistant: " + response)
            # response = "I'm sorry, I don't know how to respond to that."
            # self.display_message("Voice Assistant: " + response)
            # self.voice_assistant.speak(response)
        except sr.UnknownValueError:
            self.display_message("Voice Assistant could not understand audio")
        except sr.RequestError as e:
            self.display_message("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)

    # create listen button
    picture = tk.PhotoImage(file="mic.png")
    listen_button = tk.Button(root, command=app.listen, image=picture, borderwidth=0)
    listen_button.place(relx=0.5, rely=0.8, anchor='center')

    root.mainloop()
