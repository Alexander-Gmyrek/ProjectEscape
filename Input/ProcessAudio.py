from openai import OpenAI
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai.api_key)

def ProcessAudio(audio_file):
    my_audio_file = open(audio_file, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=my_audio_file, 
        response_format="text"
    )
    my_audio_file.close()
    return transcript