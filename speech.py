import speech_recognition as sr


def mock_recognize_speech():
    """Assiuming the speech text recognize correctly and return response """
    transcription = input("How may I help you ? : ")
    response = {
        "success": True,
        "error": None,
        "transcription": transcription
    }
    return response


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
        if response['transcription'] is None:
            response['success'] = False
    except sr.RequestError:
        response["success"] = False
        response["error"] = "Please check your internet connection."
    except sr.UnknownValueError:
        # speech was unintelligible
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response
