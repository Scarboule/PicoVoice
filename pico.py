from picovoice import Picovoice
import numpy as np
import pyaudio

with open("acceskey.txt", 'r') as f:
    key = f.read()


RATE = 16000
CHUNK_SIZE = 512



def wake_word_callback():
    # wake word detected
    print("Wake Word detecté ..")
    pass

def calcul(s):

    if len(s) == 3:

        o = s['opérateur'],
        a = s["chiffre1"],
        b = s["chiffre2"],

        if o == 'fois':
            return a * b
    else:
        print("Je n'ai pas tout compris...")


def inference_callback(inference):
    if inference.is_understood:
        intent = inference.intent
        slots = inference.slots
        # take action based on intent and slot values
        print(inference)
        print("jjj")
        print(intent)
        print(slots)
        calcul(slots)
    else:
        # unsupported command
        print(inference)
        pass

print("Init...")

handle = Picovoice(
    access_key=key,
    keyword_path = "calcul.ppn",
    wake_word_callback = wake_word_callback,
    context_path = "calcul.rhn",
    inference_callback = inference_callback,
    porcupine_model_path="porcupine_params_fr.pv",
    rhino_model_path="rhino_params_fr.pv"
)


print("connecting to mic ...")

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

def get_next_audio_frame():
    audio_frame = stream.read(CHUNK_SIZE)
    audio_frame = np.frombuffer(audio_frame, dtype=np.int16)
    return audio_frame

print("listening ...")

while True:
    audio_frame = get_next_audio_frame()
    handle.process(audio_frame)


