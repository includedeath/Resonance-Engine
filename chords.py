import numpy as np
import sounddevice as sd
from chorddict import detect_chord

fs=44100
duration=1
history=[]

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
    max_freq=1200
    max_index=int(max_freq*len(audio)/fs)
    magnitude=magnitude[:max_index]

    threshold=max(magnitude)*0.3
    indices=np.where(magnitude>threshold)[0]

    freqs=[]
    for i in indices:
        f=i*fs/len(audio)
        if f>50:
            freqs.append(f)

    filtered=[]
    for f in sorted(freqs):
        if all(abs(f/x-round(f/x))>0.1 for x in filtered):
            filtered.append(f)
    filtered=filtered[:4]

    return filtered

print("Play a chord... Press Ctrl+C to stop\n")
print(detect_chord(["C","E"]))

try:
    while True:
        freqs=detect()

        if freqs:
            notes_detected=[freq_to_note(f) for f in freqs]
            notes_simple=[n[:-1] for n in notes_detected]

            history.append(notes_simple)
            if len(history)>5:
                history.pop(0)

            all_notes=[n for h in history for n in h]
            notes_simple=list(set(all_notes))

            chord,confidence=detect_chord(notes_simple)

            print("\nNotes:",notes_simple)
            print("Chord:",chord,"| Confidence:",confidence)

except KeyboardInterrupt:
    print("\nStopped")