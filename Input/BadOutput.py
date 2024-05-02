from pathlib import Path
from openai import OpenAI
import openai
import os


# Initialize the OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai.api_key)

def convert_text_to_speech(text, language, voice, model_name, audio_file):
    switcher = {
        "default": openai_tts,
    }

    func = switcher.get(model_name, lambda: "Invalid model")

    return func(text, language, voice, audio_file)

def openai_tts(text, language, voice, audio_file):
    if not isinstance(text, str):
            text = str(text)
    try:
        response = client.audio.speech.create(
            model="tts-1",  
            voice=voice,
            input=text
        )

        speech_file_path = Path.cwd() / audio_file
        response.stream_to_file(speech_file_path)


        return speech_file_path
    except Exception as e:
        return str(e)




    
#encoded_audio_data = convert_text_to_speech("Today is a wonderful day to build something people love!", "en-US", "onyx", "default")
#print(encoded_audio_data)
