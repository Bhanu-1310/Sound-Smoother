# importing the necessary libraries
import pyaudio
import wave


# set the parameters for the audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = int(input("Set recording time (in sec): "))  # set the duration of the recording
WAVE_OUTPUT_FILENAME = "output.wav"  ## iss naam se save hogi file


# create an instance of the PyAudio class
p = pyaudio.PyAudio()


# open the microphone for recording
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

# read audio input stream into byte string\
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)


# stop the stream and close the PyAudio instance
stream.stop_stream()
stream.close()
p.terminate()

print("Finished recording.")

# save the recorded audio to a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
