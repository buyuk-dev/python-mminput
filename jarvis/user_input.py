import sys
import multiprocessing
import time
import fcntl
import os

from .interface import audio_input


def text_input_proc(queue):
    sys.stdin = open(0)
    result = input()
    queue.put(result)


def audio_input_proc(queue):
    result = audio_input()
    queue.put(result)


def prompt_user(prompt: str) -> str:
    print(prompt)

    queue = multiprocessing.Queue()

    # Create processes for stdin and audio input
    stdin_process = multiprocessing.Process(target=text_input_proc, args=(queue,))
    audio_process = multiprocessing.Process(target=audio_input_proc, args=(queue,))

    # Start both processes
    stdin_process.start()
    audio_process.start()

    # Wait for either process to put data in the queue
    result = queue.get()

    # Terminate both processes
    stdin_process.terminate()
    audio_process.terminate()

    return result


# Example usage
if __name__ == "__main__":
    result = prompt_user("Please provide input (text or audio): ")
    print(f"You said: {result}")
