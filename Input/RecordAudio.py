import pyaudio
import wave
import webrtcvad
import collections
import sys
import numpy as np
from scipy.signal import butter, lfilter


FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate
CHUNK_DURATION_MS = 30  # Each read length in milliseconds
PADDING_DURATION_MS = 1500  # Amount of silence to signify the end of a phrase
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # Chunk to read
CHUNK_BYTES = CHUNK_SIZE * 2  # Bytes in a chunk
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # Number of chunks in a window
OUTPUT_FILENAME = "recorded_audio.wav"

vad = webrtcvad.Vad(3)

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def record_audio(output_filename):
    OUTPUT_FILENAME = output_filename
    # Set up audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    
    print("Please start speaking.")
    
    frames = []
    num_silent_chunks = 0
    triggered = False

    try:
        while True:
            chunk = stream.read(CHUNK_SIZE)
            chunk = np.frombuffer(chunk, dtype=np.int16)
            filtered_chunk = highpass_filter(chunk, cutoff=100, fs=RATE)
            filtered_chunk = filtered_chunk.astype(np.int16).tobytes()
            active = vad.is_speech(filtered_chunk, RATE)

            sys.stdout.write('1' if active else '0')
            sys.stdout.flush()

            if not triggered:
                frames.append(chunk)
                num_window_chunks = len(frames)
                if num_window_chunks > NUM_WINDOW_CHUNKS:
                    frames.pop(0)
                    num_window_chunks -= 1

                if active and num_window_chunks == NUM_WINDOW_CHUNKS:
                    sys.stdout.write('+(%s)' % (num_window_chunks * CHUNK_DURATION_MS))
                    triggered = True
                    start = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE / 1000)
                    frames = frames[-NUM_WINDOW_CHUNKS:]
            else:
                frames.append(chunk)
                if not active:
                    num_silent_chunks += 1
                    if num_silent_chunks > NUM_PADDING_CHUNKS:
                        break
                else:
                    num_silent_chunks = 0
    finally:
        print("\nRecording finished.")
        stream.close()
        p.terminate()

        # Save the audio data
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f"Audio saved to {OUTPUT_FILENAME}")