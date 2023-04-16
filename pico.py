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

def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

def calcul(s):
    def frToInt(n):
            nombres = {'un': 1, 'deux': 2, 'trois': 3, 'quatre': 4, 'cinq': 5, 'six': 6, 'sept': 7, 'huit': 8, 'neuf': 9, 'dix': 10, 'zéro': 0}
            if n in nombres:
                return nombres[n]  
    if len(s) == 3:
        e = s["opérateur"],
        o = convertTuple(e)

        if o == 'fois':
            print((frToInt(s["chiffre1"]) * frToInt(s["chiffre2"])))
        elif o == ('plus'):
            print((frToInt(s["chiffre1"]) + frToInt(s["chiffre2"])))
        elif o == 'moins':
            print((frToInt(s["chiffre1"]) - frToInt(s["chiffre2"])))
    else:
        print("Je n'ai pas tout compris...")


def inference_callback(inference):
    if inference.is_understood:
        intent = inference.intent
        slots = inference.slots
        print(slots['chiffre1'])
        print(slots['opérateur'])
        print(slots['chiffre2'])
        print("égale")
        
        calcul(slots)
        print('')
        
    else:

        print("Je n'ai pas tout compris...")
        pass
    print("still listening ...")

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

print('Dites "calcul" puis une opération, une multiplication, ou une soustraction entre deux chiffre entier entre 0 et 10')
print('')
print("listening ...")

while True:
    audio_frame = get_next_audio_frame()
    handle.process(audio_frame)


