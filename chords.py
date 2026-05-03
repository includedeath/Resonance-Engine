import numpy as np
import sounddevice as sd
from chorddict import detect_chord

fs=44100
duration=1

notes=["C","C#","D","D#","E","F",
       "F#","G","G#","A","A#","B"]

def freq_to_note(f):
    A4=440
    n=12*np.log2(f/A4)
    n=round(n)
    note_index=(n+9)%12
    octave=4+(n+9)//12
    return notes[note_index]+str(octave)

def detect():
    audio=sd.rec(int(duration*fs),samplerate=fs,channels=1)
    sd.wait()
    audio=audio.flatten()
    audio=audio*np.hanning(len(audio))

    fft=np.fft.fft(audio)
    magnitude=np.abs(fft)
    magnitude=magnitude[:len(magnitude)//2]

    magnitude[:20]=0

    indices=np.argsort(magnitude)[-10:]

    freqs=[]
    for i in indices:
        f=i*fs/len(audio)
        if f>50:
            freqs.append(f)

    filtered=[]
    for f in sorted(freqs):
        if all(abs(f-2*x)>5 for x in filtered):
            filtered.append(f)

    return filtered

print("Play a chord... Press Ctrl+C to stop\n")

try:
    while True:
        freqs=detect()

        if freqs:
            freqs=[round(f,1) for f in freqs]
            notes_detected=[freq_to_note(f) for f in freqs]

            notes_simple=[n[:-1] for n in notes_detected]
            notes_simple=list(set(notes_simple))

            chord=detect_chord(notes_simple)

            print("Notes:",notes_simple)
            print("Chord:",chord)

except KeyboardInterrupt:
    print("\nStopped")