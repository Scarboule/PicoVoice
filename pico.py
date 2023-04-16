from picovoice import Picovoice
import numpy as np
import pyaudio

with open("acceskey.txt", 'r') as f:
    key = f.read()

RATE = 16000
CHUNK_SIZE = 512



def wake_word_callback():
    # wake word detected
    print("detect")
    pass


def inference_callback(inference):
    if inference.is_understood:
        intent = inference.intent
        slots = inference.slots
        # take action based on intent and slot values
        print(inference)
        print("jjj")
        print(intent)
        print(slots)
    else:
        # unsupported command
        print(inference)
        pass


handle = Picovoice(
    access_key=key,
    keyword_path = "ok google_windows.ppn",
    wake_word_callback = wake_word_callback,
    context_path='alarm_windows.rhn',
    inference_callback = inference_callback
)



p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

def get_next_audio_frame():
    """
    Récupère le prochain cadre audio à partir du microphone et le renvoie sous forme de tableau d'échantillons.
    """
    audio_frame = stream.read(CHUNK_SIZE)
    audio_frame = np.frombuffer(audio_frame, dtype=np.int16)
    return audio_frame

while True:
    audio_frame = get_next_audio_frame()
    handle.process(audio_frame)


