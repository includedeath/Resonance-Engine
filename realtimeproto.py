import numpy as np
import sounddevice as sd

fs=44100
duration=0.5
notes=["C","C#","D","D#","E","F",
       "F#","G","G#","A","A#","B"]
A4=440
history=[]
last_note=None
print("Real-time tuner started (Ctrl+C to stop)\n")
try:
    while True:
        audio=sd.rec(int(duration*fs),samplerate=fs,channels=1)
        sd.wait()
        audio=audio.flatten()
        fft=np.fft.fft(audio)
        magnitude=np.abs(fft)
        half=len(magnitude)//2
        magnitude=magnitude[:half]
        magnitude[:20]=0
        index=np.argmax(magnitude)
        frequency=index*fs/len(audio)
        if frequency<80: #ignoring low frequency noise
            continue
        history.append(frequency)

        if len(history)>5:
            history.pop(0)
        frequency=sum(history)/len(history)
        frequency=round(frequency,1)
        n=round(12*np.log2(frequency/A4))
        note_index=(n+9)%12
        note=notes[note_index]
        octave=4+(n+9)//12
        exact_freq=A4*(2**(n/12))
        error=frequency-exact_freq
        if abs(error)<1:
            status="In Tune"
        elif error>0:
            status="Sharp"
        else:
            status="Flat"
        current_note=note+str(octave)
        if current_note!=last_note:
            print(f"{current_note}|{frequency}Hz|{status}")
            last_note=current_note
except KeyboardInterrupt:
    print("\nStopper tuner")

