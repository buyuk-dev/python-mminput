import whisper
import pyaudio
import wave
import numpy as np

# Initialize the Whisper model
model = whisper.load_model("base.en")

def is_silent(data, threshold=500):
    """Returns 'True' if below the threshold"""
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.abs(audio_data).mean() < threshold

def record_audio(file_path, silence_threshold=500, silence_duration=3.0):
    # Set up audio recording parameters
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames
    silence_chunks = 0  # Number of chunks with silence
    silence_chunk_threshold = int(fs / chunk * silence_duration)

    while True:
        data = stream.read(chunk)
        frames.append(data)

        if is_silent(data, threshold=silence_threshold):
            silence_chunks += 1
        else:
            silence_chunks = 0

        if silence_chunks > silence_chunk_threshold:
            break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(file_path):
    # Use Whisper model to transcribe the audio file
    result = model.transcribe(file_path)
    return result['text']

def main():
    audio_file = "output.wav"
    record_audio(audio_file, silence_threshold=500, silence_duration=3.0)
    transcription = transcribe_audio(audio_file)
    print(f"Transcription: {transcription}")

if __name__ == "__main__":
    main()
