import numpy as np
import sounddevice as sd
import tkinter as tk

guitar_tuning={"E2":82.41,"A2":110.00,"D3":146.83,
               "G3":196.00,"B3":246.94,"E4":329.63}

ukulele_tuning={"G4":392.00,"C4":261.63,
                "E4":329.63,"A4":440.00}

instrument=input("Choose instrument (g/u): ").lower()
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

# -------- UI --------
root=tk.Tk()
root.title("Tuner")
root.configure(bg="black")

label_note=tk.Label(root,text=f"Tuning {target_note}",
                    font=("Arial",18),bg="black",fg="white")
label_note.pack(pady=10)

label_freq=tk.Label(root,text="0 Hz",
                    font=("Arial",16),bg="black",fg="white")
label_freq.pack(pady=5)

canvas=tk.Canvas(root,width=400,height=120,bg="black",highlightthickness=0)
canvas.pack()

center_line=200

def update_ui(frequency):
    canvas.delete("all")

    error=frequency-target_freq
    pos=center_line+(error*5)

    if pos<0:
        pos=0
    if pos>400:
        pos=400

    # center (perfect)
    canvas.create_line(center_line,0,center_line,120,fill="#00ff88",width=3)

    # pointer
    color="#00ff88" if abs(error)<0.5 else "#ff4444"
    canvas.create_line(pos,0,pos,120,fill=color,width=5)

    label_freq.config(text=f"{round(frequency,1)} Hz")

    root.update()

# -------- AUDIO --------
def detect():
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
        return None

    index=start+np.argmax(local_segment)
    frequency=index*fs/len(audio)

    return frequency

def loop():
    freq=detect()
    if freq:
        update_ui(freq)
    root.after(100,loop)

loop()
root.mainloop()