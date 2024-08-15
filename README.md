# Jarvis

This project contains a script that records audio, detects silence to stop recording, and transcribes the recorded audio using the Whisper model.

## Files

- `jarvis.py`: Main script to record and transcribe audio.
- `Pipfile` and `Pipfile.lock`: Dependency management files.

## Requirements

- `whisper`
- `pyaudio`
- `numpy`

## Usage

1. Ensure you have the required dependencies installed. You can use the Pipfile to create a virtual environment with the necessary packages:

    **Note for macOS users with M1/M3 chips**: If you encounter issues installing `pyaudio`, you may need to install the `portaudio` library via Homebrew and set the environment variables before installing `pyaudio`. Here are the steps:

    ```sh
    brew install portaudio
    pipenv install
    ```

2. Run the script:

    ```sh
    pipenv run python jarvis.py
    ```

The script will start recording audio. It will stop recording when it detects silence for a specified duration and then transcribe the recorded audio.
