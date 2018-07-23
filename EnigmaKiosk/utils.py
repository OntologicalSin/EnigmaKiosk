import speech_recognition as sr

class SpeechRec:

    @staticmethod
    def smth(binary):

        r = sr.Recognizer()
        with sr.AudioFile("file.wav") as source:
            audio = r.record(source)
        text = "null"
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            text = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        print(text)
        return text

