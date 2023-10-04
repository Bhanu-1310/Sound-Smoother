from scipy.io import wavfile
import numpy as np
from scipy.signal import wiener
import matplotlib.pyplot as plt

# read the audio file
filename = "output.wav"
sample_rate, audio_array = wavfile.read(filename)

# scale the audio signal to a higher range
max_value = np.max(np.abs(audio_array))
audio_array = audio_array.astype(np.float32) / max_value

# apply the Wiener filter to the audio signal
filtered_signal = wiener(audio_array,5005,0.001)

# scale the filtered signal back to the original range
filtered_signal = (filtered_signal * max_value).astype(np.int16)

# save the filtered signal to a new audio file
wavfile.write("output_audio.wav", sample_rate, filtered_signal)


# visualization
fig, (ax_orig, ax_filt) = plt.subplots(2, 1, sharex=True)
t = np.arange(len(audio_array)) / sample_rate

ax_orig.plot(t, audio_array, 'r-', linewidth=1, label='Original')
ax_orig.legend()

ax_filt.plot(t, filtered_signal, 'b-', linewidth=1, label='Wiener filtered')
ax_filt.legend()

ax_orig.set_xlabel('Time [s]')
ax_orig.set_ylabel('Amplitude')
ax_filt.set_xlabel('Time [s]')
ax_filt.set_ylabel('Amplitude')

plt.show()

# plot the spectrograms of the original and filtered signals
fig, (ax_orig, ax_filt) = plt.subplots(2, 1, sharex=True)
ax_orig.specgram(audio_array, Fs=sample_rate, cmap='jet')
ax_orig.set_xlabel('Time [s]')
ax_orig.set_ylabel('Frequency [Hz]')
ax_orig.set_title('Original')

ax_filt.specgram(filtered_signal, Fs=sample_rate, cmap='jet')
ax_filt.set_xlabel('Time [s]')
ax_filt.set_ylabel('Frequency [Hz]')
ax_filt.set_title('Wiener filtered')

plt.show()

# histro
fig, (ax_orig, ax_filt, ax_hist) = plt.subplots(3, 1, sharex=True)
ax_orig.plot(t, audio_array, 'r-', linewidth=1, label='Original')
ax_filt.plot(t, filtered_signal, 'b-', linewidth=1, label='Wiener filtered')
ax_orig.legend()
ax_filt.legend()
ax_orig.set_xlabel('Time [s]')
ax_orig.set_ylabel('Amplitude')
ax_filt.set_xlabel('Time [s]')
ax_filt.set_ylabel('Amplitude')
ax_hist.hist(audio_array, bins=100, alpha=0.5, label='Original')
ax_hist.hist(filtered_signal, bins=100, alpha=0.5, label='Wiener filtered')
ax_hist.legend()
ax_hist.set_xlabel('Amplitude')
ax_hist.set_ylabel('Count')
plt.show()

# psd
from scipy.signal import welch

f_orig, Pxx_orig = welch(audio_array, fs=sample_rate, nperseg=1024)
f_filt, Pxx_filt = welch(filtered_signal, fs=sample_rate, nperseg=1024)

fig, ax = plt.subplots()
ax.semilogy(f_orig, Pxx_orig, 'r-', linewidth=1, label='Original')
ax.semilogy(f_filt, Pxx_filt, 'b-', linewidth=1, label='Wiener filtered')
ax.legend()
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Power spectral density')
plt.show()

#spectrogram
diff = audio_array - filtered_signal
fig, ax = plt.subplots()
ax.specgram(diff, Fs=sample_rate, cmap='jet')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Frequency [Hz]')
ax.set_title('Difference between original and Wiener filtered')
plt.show()
