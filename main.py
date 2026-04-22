import librosa
import matplotlib.pyplot as plt
import numpy as np


#loading of the audio file
audio,sr=librosa.load("sample1.wav")

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

print("Dominant Frequency is:",frequency)
A4=440  #reference frequency
n=12*np.log2(frequency/A4)
n=round(n)
notes=["C","C#","D","D#","E","F",
       "F#","G","G#","A","A#","B"]
note_index=(n+9)%12
note=notes[note_index]
octave=4+(n+9)//12
print("Detected Note:",note+str(octave))

