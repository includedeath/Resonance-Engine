import librosa
import matplotlib.pyplot as plt
import numpy as np


#loading of the audio file 
audio,sr=librosa.load("sample3.wav")
threshold=0.02
indices=np.where(np.abs(audio)>threshold)[0]
if len(indices)==0:
    print("No strong signal detected")
    exit()
start=indices[0]
audio=audio[start:start+40000]
#basic display
#print("Sample rate:",sr)
#print("First 10 samples:",audio[:10])
#print("Total samples:",len(audio))


#basic waveform using matplot library
#plt.plot(audio)
#plt.title("Waveform")
#plt.xlabel("Samples")
#plt.ylabel("Amplitude")
#plt.show()

#fast fourier transform
fft=np.fft.fft(audio)
magnitude=np.abs(fft)
half=len(magnitude)//2
magnitude=magnitude[:half]
index=np.argmax(magnitude)

frequency=index*sr/len(audio)

A4=440  #reference frequency
n=12*np.log2(frequency/A4)
n=round(n)
notes=["C","C#","D","D#","E","F",
       "F#","G","G#","A","A#","B"]
note_index=(n+9)%12
note=notes[note_index]
octave=4+(n+9)//12

#tuning error
exact_freq=A4*(2**(n/12))
error=frequency-exact_freq
if abs(error)<1:
    status="In Tune"
elif error>0:
    status="Sharp"
else:
    status="Flat"
print("Frequency:",frequency)
print("Detected Note:",note+str(octave))
print("Error:",round(error,2),"Hz")
print("Status:",status)

