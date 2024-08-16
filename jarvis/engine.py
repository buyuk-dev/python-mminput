import whisper
import wave
import pyaudio
import numpy as np
import io
import tempfile
import logging

# Initialize the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

# Initialize the Whisper model
model = whisper.load_model("base.en")


def is_silent(data, threshold=500):
    """Returns 'True' if below the threshold"""
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.abs(audio_data).mean() < threshold


def record_audio(
    silence_threshold=500,
    silence_duration=3.0,
    initial_silence_timeout=10.0,
    target_sample_rate=16000,
):
    # Set up audio recording parameters
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = target_sample_rate  # Record at the target sample rate

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    logger.info("Recording")

    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )

    frames = []  # Initialize array to store frames
    silence_chunks = 0  # Number of chunks with silence
    silence_chunk_threshold = int(fs / chunk * silence_duration)
    initial_silence_chunks = int(fs / chunk * initial_silence_timeout)
    sound_detected = False

    while True:
        data = stream.read(chunk)
        frames.append(data)

        if not sound_detected:
            if not is_silent(data, threshold=silence_threshold):
                sound_detected = True
            else:
                if len(frames) > initial_silence_chunks:
                    frames = []  # reset frames if initial silence exceeds timeout
        else:
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

    logger.info("Finished recording")

    audio_data = b"".join(frames)
    return audio_data, sample_format, channels, fs


def transcribe_audio_with_tempfile(audio_data, sample_format, channels, fs):
    # Create a temporary file for the audio data
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
        wf = wave.open(temp_audio_file, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(audio_data)
        wf.close()

        # Use Whisper model to transcribe the audio data from the file path
        result = model.transcribe(temp_audio_file.name)
        return result["text"]


def transcribe_audio_with_ndarray(audio_data, sample_format, channels, fs):
    # Convert the audio data to a numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

    # Ensure the audio is in mono by averaging channels if necessary
    if channels > 1:
        audio_array = audio_array.reshape(-1, channels).mean(axis=1)

    # Use Whisper model to transcribe the audio data from the numpy array
    result = model.transcribe(audio_array, fp16=False)
    return result["text"]


def main():
    audio_data, sample_format, channels, fs = record_audio(
        silence_threshold=500, silence_duration=3.0, initial_silence_timeout=10.0
    )
    # transcription_tempfile = transcribe_audio_with_tempfile(audio_data, sample_format, channels, fs)
    # print(f"Transcription with tempfile: {transcription_tempfile}")

    transcription_ndarray = transcribe_audio_with_ndarray(
        audio_data, sample_format, channels, fs
    )
    print(f"Transcription with ndarray: {transcription_ndarray}")


if __name__ == "__main__":
    main()
