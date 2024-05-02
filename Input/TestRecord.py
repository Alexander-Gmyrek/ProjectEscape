import os
from pydub import AudioSegment
from pydub.silence import detect_silence
from scipy.io import wavfile
import numpy as np
from pydub.silence import detect_nonsilent, detect_silence

def is_file_size_too_small(file_path, min_size_bytes=1024):
    return os.path.getsize(file_path) < min_size_bytes

def is_duration_too_short(file_path, min_duration_seconds=1):
    audio = AudioSegment.from_file(file_path)
    return len(audio) < min_duration_seconds * 1000  # Duration in milliseconds
'''
def is_mostly_silence(file_path, silence_threshold=-50.0, min_silence_duration=1000):
    audio = AudioSegment.from_file(file_path)

    nonsilent_segments = detect_nonsilent(audio, min_silence_len=min_silence_duration, silence_thresh=silence_threshold)
    
    # Check if there are any nonsilent segments
    if nonsilent_segments:
        start_of_sound = nonsilent_segments[0][0]  # Start of the first sound
        # Consider only the part of the audio after the first sound
        audio_after_sound = audio[start_of_sound:]
    else:
        # If there are no nonsilent segments, the whole file is silent
        return True

    # Detect silence in the audio after the initial sound
    silence = detect_silence(audio_after_sound, min_silence_len=min_silence_duration, silence_thresh=silence_threshold)
    total_silence = sum(duration for start, duration in silence)
    
    # Return True if more than 90% of the audio after the initial sound is silence
    return total_silence >= len(audio_after_sound) * 0.9
'''
def is_average_volume_too_low(file_path, volume_threshold=-50.0):
    audio = AudioSegment.from_file(file_path)
    return audio.dBFS < volume_threshold

def is_audio_content_insufficient(file_path, threshold_value=1000):
    sample_rate, data = wavfile.read(file_path)
    magnitude = np.abs(np.fft.rfft(data))
    frequency = np.fft.rfftfreq(len(data), d=1/sample_rate)
    significant_content = sum(mag for mag, freq in zip(magnitude, frequency) if freq > 20)
    return significant_content < threshold_value

def test_recording(file_path):
    failed_tests = []

    if is_file_size_too_small(file_path):
        failed_tests.append("File Size Too Small")

    if is_duration_too_short(file_path):
        failed_tests.append("Duration Too Short")

    #if is_mostly_silence(file_path):
    #    failed_tests.append("Mostly Silence")

    if is_average_volume_too_low(file_path):
        failed_tests.append("Average Volume Too Low")

    if is_audio_content_insufficient(file_path):
        failed_tests.append("Audio Content Insufficient")

    if failed_tests:
        for test in failed_tests:
            print(f"Test Failed: {test}")
        return -1
    else:
        print("All tests passed.")
        return 0