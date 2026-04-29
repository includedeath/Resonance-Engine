import numpy as np
import sounddevice as sd
import sys

guitar_tuning={"E2":82.41,"A2":110.00,"D3":146.83,
               "G3":196.00,"B3":246.94,"E4":329.63}

ukulele_tuning={"G4":392.00,"C4":261.63,
                "E4":329.63,"A4":440.00}

instrument=input("Choose instrument (guitar/ukulele): ").lower()
if instrument=="g":
    tuning=guitar_tuning
elif instrument=="u":
    tuning=ukulele_tuning
else:
    print("Invalid choice")
    exit()

print("Available strings:",list(tuning.keys()))
target_note=input("Which string are you tuning? ").upper()

if target_note not in tuning:
    print("Invalid string")
    exit()

target_freq=tuning[target_note]

fs=44100
duration=1
history=[]

print(f"\nTuning {target_note} ({target_freq} Hz)")
print("Real-time tuner started (Ctrl+C to stop)\n")

try:
    while True:
        audio=sd.rec(int(duration*fs),samplerate=fs,channels=1)
        sd.wait()
        audio=audio.flatten()
        audio=audio*np.hanning(len(audio))

        fft=np.fft.fft(audio)
        magnitude=np.abs(fft)
        magnitude=magnitude[:len(magnitude)//2]
        magnitude[:20]=0

        target_index=int(target_freq*len(audio)/fs)
        window=80

        start=max(0,target_index-window)
        end=min(len(magnitude),target_index+window)

        local_segment=magnitude[start:end]

        if np.max(local_segment)<np.mean(magnitude)*2:
            continue

        local_index=np.argmax(local_segment)
        index=start+local_index

        frequency=index*fs/len(audio)

        if frequency<50:
            continue

        history.append(frequency)
        if len(history)>3:
            history.pop(0)

        frequency=sum(history)/len(history)

        error=frequency-target_freq

        if abs(error)<0.5:
            status="Perfect"
            direction=""
        elif abs(error)<2:
            status="Good"
            direction="Tighten" if error<0 else "Loosen"
        elif error>0:
            status="Too High"
            direction="Loosen"
        else:
            status="Too Low"
            direction="Tighten"

        if direction:
            msg=f"{status} ({direction})"
        else:
            msg=status

        sys.stdout.write(f"\r{round(frequency,1)} Hz | {msg}")
        sys.stdout.flush()

except KeyboardInterrupt:
    print("\nStopped tuner")