import numpy as np
import wave
import pyaudio
from pydub import AudioSegment
from scipy.signal import butter, lfilter, resample

# Function to apply a band-pass filter
def band_pass_filter(data, lowcut, highcut, rate, order=5):
    nyq = 0.5 * rate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

# Function to add subtle noise
def add_noise(data, noise_level=0.001):
    noise = np.random.randn(len(data))
    augmented_data = data + noise_level * np.max(data) * noise
    return augmented_data

def pitch_shift(audio_data, shift):
    return resample(audio_data, len(audio_data) + shift)

# Function to process an MP3 file
def process_audio_file(file_path, output_path):
    # Load the MP3 file
    audio = AudioSegment.from_file(file_path)
    
    # Convert to mono and sample rate of 44100 if not already
    if audio.channels > 1:
        audio = audio.set_channels(1)
    if audio.frame_rate != 44100:
        audio = audio.set_frame_rate(44100)
    
    # Convert to numpy array
    samples = np.array(audio.get_array_of_samples())

    # Apply band-pass filter
    filtered_audio = band_pass_filter(samples, 200, 3400, 44100)
    
    # Add noise
    noisy_audio = add_noise(filtered_audio)

    pitch_shifted_audio = pitch_shift(noisy_audio, 75)
    
    # Convert numpy array back to AudioSegment
    processed_audio = audio._spawn(pitch_shifted_audio.astype(np.int16).tobytes())
    
    # Export the processed audio to a new file
    processed_audio.export(output_path, format="mp3")