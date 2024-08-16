from .engine import record_audio, transcribe_audio_with_ndarray

class VoiceRecorder:
    def __init__(self, silence_threshold=500, silence_duration=3.0, initial_silence_timeout=10.0, target_sample_rate=16000):
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.initial_silence_timeout = initial_silence_timeout
        self.target_sample_rate = target_sample_rate
        self.audio_data = None
        self.sample_format = None
        self.channels = None
        self.fs = None

    def start_recording(self):
        print("Start recording")
        # Start recording audio using the record_audio function from engine.py
        self.audio_data, self.sample_format, self.channels, self.fs = record_audio(
            silence_threshold=self.silence_threshold,
            silence_duration=self.silence_duration,
            initial_silence_timeout=self.initial_silence_timeout,
            target_sample_rate=self.target_sample_rate
        )

    def stop_recording(self):
        print("Stop recording")
        # Stops recording and returns audio data
        return self.audio_data, self.sample_format, self.channels, self.fs


class Transcriber:
    def __init__(self, method="ndarray"):
        self.method = method

    def transcribe(self, audio_data):
        # Transcribe the given audio data using the transcribe_audio_with_ndarray function from engine.py
        audio_data, sample_format, channels, fs = audio_data
        if self.method == "ndarray":
            return transcribe_audio_with_ndarray(audio_data, sample_format, channels, fs)
        else:
            raise ValueError(f"Unsupported transcription method: {self.method}")


class VoiceInput:
    def __init__(self, recorder_config=None, transcriber_config=None):
        # Use default configurations if none provided
        if recorder_config is None:
            recorder_config = {
                "silence_threshold": 500,
                "silence_duration": 3.0,
                "initial_silence_timeout": 10.0,
                "target_sample_rate": 16000
            }
        if transcriber_config is None:
            transcriber_config = {
                "method": "ndarray"
            }
        self.recorder = VoiceRecorder(**recorder_config)
        self.transcriber = Transcriber(**transcriber_config)

    def record_and_transcribe(self):
        self.recorder.start_recording()
        audio_data = self.recorder.stop_recording()
        return self.transcriber.transcribe(audio_data)


def audio_input():
    """A high-level function to record and transcribe audio with default settings."""
    voice_input = VoiceInput()
    return voice_input.record_and_transcribe()

