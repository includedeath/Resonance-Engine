import librosa
import matplotlib.pyplot as plt
#loading of the audio file
audio,sr=librosa.load("sample1.wav")
#basic display
print("Sample rate:",sr)
print("First 50 samples:",audio[:50])
print("Total samples:",len(audio))

plt.plot(audio)
plt.title("Waveform")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.show()
