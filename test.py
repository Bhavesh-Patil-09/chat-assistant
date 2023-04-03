from neuralmodel import GenericAssistant
from bot import VoiceAssistant

if __name__ == "__main__":
    chatbot = VoiceAssistant()
    mappings = {
        "notes": chatbot.make_note,
        "googlesearch": chatbot.google_search,
        "music": chatbot.play_youtube,
        "wikipedia": chatbot.search_info,
        "goodbye": chatbot.quit,
        "apps": chatbot.launch_apps,
        "launch-website": chatbot.open_website,
        "news":chatbot.get_news,
        "screenshot":chatbot.snapshot,
        "selfi":chatbot.capture_photo,
        "system": chatbot.system_status,
        "weather": chatbot.get_weather,
        "datetime": chatbot.current_datetime,
        "locationdistance": chatbot.calc_location_difference
        }
    assistant = GenericAssistant('dataset.json', mappings)
    # assistant.train_model()
    # assistant.save_model()

    assistant.load_model()
    myintents = ["find the distance"]
    # myintents = [
    #     "hi",
    #     "hey how are you", 
    #     "search website", 
    #     "launch whatsapp", 
    #     "make me laugh", 
    #     "capture scrrenshot", 
    #     "snapshot please", 
    #     "take selfi",
    #     "you are cool",
    #     "can you search for me",
    #     "what is status of weather",
    #     "what is today date",
    #     "please take a note",
    #     "my system status please",
    #     "I want to hear some news",
    #     "play some music",
    #     "what is your name",
    #     "bye bye",
    #     ]

    for i in myintents:
        response = assistant.request(i)
        if response is not None:
            chatbot.speak(response)
    import sys
    sys.exit(0)

