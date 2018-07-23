from gtts import gTTS
from pydub import AudioSegment

file_location='saythis.mp3'

def text_to_speech(text):
    tts = gTTS(text, lang='en')
    tts.save(file_location)
    # song = AudioSegment.from_mp3("saythis.mp3")
    # song = song + 36
    # song.export("saythis.mp3", "mp3")