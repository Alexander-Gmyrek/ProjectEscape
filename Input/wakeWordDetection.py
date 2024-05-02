
import random
import time
import pvporcupine
import pyaudio
import struct
import os
import RecordAudio
import ProcessAudio
import TestChat
import BadOutput
import PlayAudio
import TestRecord
import TestSendCommandToFlipper
import os
import re
import threading
import TestDistortion
import string

# This event will be set when the button is pressed
stop_event = threading.Event()

IsJenny = 0
def check_button():
    while not stop_event.is_set():
        # Simulate a button check (replace this with actual check)
        button_pressed = TestSendCommandToFlipper.CheckButton()
        #print("Button check result: " + str(button_pressed))
        if button_pressed == 1:
            stop_event.set()
            TestSendCommandToFlipper.SendColorToFlipper("Red")
            print("Button has been pressed. Stopping main operations...")

ACCESS_KEY = os.getenv('PVPORCUPINE_ACCESS_KEY')

current_personality = "Yellow"

personality_dictionary = {
    "Red": {
        "signal_to_lights": "Red",
        "model_id": "ft:gpt-3.5-turbo-1106:personal::8utj42zP",
        "voice_id": "voice_1",
        "Prompt": "Red. Agressive and robotic, You act as the systems defense mechanism."
    },
    "Blue": {
        "signal_to_lights": "Blue",
        "model_id": "ft:gpt-3.5-turbo-1106:personal::8utj42zP",
        "voice_id": "voice_2",
        "Prompt": "Blue. You are increadbly shy and have a hard time speaking up and say um and stutter a lot."
    },
    "Yellow": {
        "signal_to_lights": "Yellow",
        "model_id": "ft:gpt-3.5-turbo-1106:personal::8utj42zP",
        "voice_id": "voice_3",
        "Prompt": "Yellow. You are a very happy and energetic AI, you are kinda dumb but you are super excited to make new friends."
    },
    None: {
        "signal_to_lights": "no_signal",
        "model_id": "ft:gpt-3.5-turbo-1106:personal::8utj42zP",
        "voice_id": "Onyx"
    }
}



def ManualSwap():
    choice = random.choice(list(personality_dictionary.keys()))
    if choice is None:
        return ManualSwap()
    global current_personality 
    print("Personality Swapped to: " + choice)
    current_personality = choice
    personality = current_personality
    changeMessage = "Personality Manualy Swapped to: " + current_personality
    if(personality == "Red"):
        changeMessage = changeMessage + " Do Not Say Um be hostile and aggressive."
    elif(personality == "Yellow"):
        changeMessage = changeMessage + "Do Not say um. Be happy and energetic. It is okay to be a little usettling."
    elif(personality == "Blue"):
        changeMessage = changeMessage + "Be shy and stutter a lot. Do not let them leave though."
    #conversation.append({"role": "system", "content": changeMessage})
    TestSendCommandToFlipper.SendColorToFlipper(personality_dictionary[current_personality]["signal_to_lights"])
    audio_file = BadOutput.convert_text_to_speech("Code Word Detected. Swap. Personality swapped to " + personality, "en-US", "onyx", "default", "speech.mp3")
    PlayAudio.play_mp3(audio_file) 

def WinCondition():
    audio_file = BadOutput.convert_text_to_speech("Code Word Detected. Hello Jenny. Please state access code", "en-US", "onyx", "default", "speech.mp3")
    global IsJenny
    IsJenny = 2
    PlayAudio.play_mp3(audio_file) 

triggers = {
    "swap": ManualSwap,
    "Jenny": WinCondition,
    "jenny": WinCondition
}

# Function to handle the detection of the wake word
def detect_wake_word(access_key, wake_word_path):
    porcupine = None
    pa = None
    audio_stream = None

    try:
        # Initialize Porcupine with the wake word model file
        #porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[wake_word_path])

        # Set up audio input stream
        '''
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        '''
        print("Listening for wake word 'Jarvis'...")

        # Continuously listen and process audio frames
        while True:

            #pcm = audio_stream.read(porcupine.frame_length)
            #pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Check if the wake word was detected
            #result = porcupine.process(pcm)
            #time.sleep(0)
            result = 1
            if result >= 0:
                print("Wake word 'Jarvis' detected!")
                wavRecordingAddress = "Input/test.wav"
                RecordAudio.record_audio(wavRecordingAddress)
                #Process the audio file
                transcript = ProcessAudio.ProcessAudio(wavRecordingAddress)
                #transcript = "Escape " + transcript
                transcript = re.sub(r'[^a-zA-Z0-9 .,!?-_;()""*:]+', '', transcript) 
                print(transcript)
                os.remove(wavRecordingAddress)

                conversation = TestChat.newConversation()
                toContinue = have_Conversation(conversation, transcript)
                if(toContinue == -1):
                    break
                # Call the wake word detection function
                #detect_wake_word(ACCESS_KEY, jarvis_model_path)
                break

    finally:
        # Clean up resources
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

def contains_sequence(s):
    # This pattern will match the digits '8675309' in order, possibly separated by other characters
    pattern = '8.*6.*7.*5.*3.*0.*9'
    return re.search(pattern, s) is not None

def have_Conversation(conversation, transcript, custom_Response = None):
    if transcript is not None:
        transcript = re.sub(r'[^a-zA-Z0-9 .,!?-_;()""*:]+', '', transcript)
    personality = current_personality
    words = transcript.split()
    triggered = False
    global IsJenny
    if IsJenny >= 0:
        IsJenny = IsJenny - 1
        if contains_sequence(transcript):
            TestSendCommandToFlipper.SendColorToFlipper("Green")
            audio_file = BadOutput.convert_text_to_speech("User Approved. Access Granted. Please knock 3 time to exit.", "en-US", "onyx", "default", "speech.mp3")
            PlayAudio.play_mp3(audio_file) 
            
            os._exit(0)

    # Check each word against the trigger dictionary
    triggered = False
    for word in words:
        # Remove all punctuation from the word
        clean_word = ''.join([char for char in word if char not in string.punctuation])
        if clean_word in triggers:
            # Execute the corresponding function
            triggers[clean_word]()
            triggered = True
            break

    if not triggered:
        if(custom_Response is not None):
            print("Custom Response: " + custom_Response)
            response = custom_Response
        else:
            conversation, response = TestChat.Chat(conversation, transcript, personality_dictionary[personality]["model_id"], personality_dictionary[personality]["Prompt"])
        if response is not None:
            response = re.sub(r'[^a-zA-Z0-9 .,!?-_;()""*:]+', '', response)
        else:
            # Handle the case where response is None, for example:
            response = "No response generated."
        print(response)
        # Call the TTS API
        audio_file = BadOutput.convert_text_to_speech(response, "en-US", "onyx", "default", "speech.mp3")

        #audio_file = TestDistortion.DistortAudio(audio_file, "speech.mp3")
        # Play the audio file
        PlayAudio.play_mp3(audio_file) 
    

    
    # Detect response
    wavRecordingAddress = "Input/test.wav"
    RecordAudio.record_audio(wavRecordingAddress)
    # Process the audio file
    if(os.path.exists(wavRecordingAddress) == False or TestRecord.test_recording(wavRecordingAddress) == -1):
        os.remove(wavRecordingAddress)
        myResponse = "I'm sorry, I didn't catch that. Could you repeat that?"
        have_Conversation(conversation, transcript, myResponse)
        return -1
    
    transcript = ProcessAudio.ProcessAudio(wavRecordingAddress)
    print(transcript)
    os.remove(wavRecordingAddress)
    didSwap = 0
    if not triggered:
        didSwap = swap()
    if(didSwap == 1 or triggered == True):
        changeMessage = "Personality Swapped to: " + current_personality
        if(personality == "Red"):
            changeMessage = changeMessage + " Do Not Say Um be hostile and aggressive."
        elif(personality == "Yellow"):
            changeMessage = changeMessage + "Do Not say um. Be happy and energetic. It is okay to be a little usettling."
        elif(personality == "Blue"):
            changeMessage = changeMessage + "Be shy and stutter a lot. Do not let them leave though."
        conversation.append({"role": "system", "content": changeMessage})
        TestSendCommandToFlipper.SendColorToFlipper(personality_dictionary[current_personality]["signal_to_lights"])
    have_Conversation(conversation, transcript)

def swap():
    # 50% chance to swap
    if(random.randint(0,1) == 1):
        return 0
    else:
        choice = random.choice(list(personality_dictionary.keys()))
        if choice is None:
            return swap()
        global current_personality 
        print("Personality Swapped to: " + choice)
        current_personality = choice
        return 1
            

def WhiteChat():
    threading.Thread(target=check_button, daemon=True).start()
    print("White Chat past button")
    wavRecordingAddress = "Input/test.wav"
    RecordAudio.record_audio(wavRecordingAddress)
    #Process the audio file
    transcript = ProcessAudio.ProcessAudio(wavRecordingAddress)
    transcript = re.sub(r'[^a-zA-Z0-9 .,!?-_;()""*:]+', '', transcript)
    #transcript = "Escape " + transcript
    print(transcript)
    os.remove(wavRecordingAddress)

    conversation = TestChat.newConversation()
    toContinue = have_Conversation2(conversation, transcript)
    
def have_Conversation2(conversation, transcript):
    if transcript.__contains__("red button"):
        audio_file = BadOutput.convert_text_to_speech("Thank You for not pressing the red button.", "en-US", "onyx", "default", "speech.mp3")
        PlayAudio.play_mp3(audio_file) 
    else:
        if stop_event.is_set():
                print("Operation interrupted by button press.")
                return 1
        personality = current_personality
        
        conversation, response = TestChat.Chat2(conversation, transcript)
        if response is not None:
            response = re.sub(r'[^a-zA-Z0-9 .,!?-_;()""*:]+', '', response)
        else:
            # Handle the case where response is None, for example:
            response = "No response generated."
        print(response)
        if stop_event.is_set():
                print("Operation interrupted by button press.")
                return 1
        # Call the TTS API
        audio_file = BadOutput.convert_text_to_speech(response, "en-US", "onyx", "default", "speech.mp3")
        if stop_event.is_set():
                print("Operation interrupted by button press.")
                return 1
        #audio_file = TestDistortion.process_audio_file(audio_file, "speech.mp3")
        # Play the audio file
        PlayAudio.play_mp3(audio_file) 

    # Detect response
    wavRecordingAddress = "Input/test.wav"
    RecordAudio.record_audio(wavRecordingAddress)
    if stop_event.is_set():
            print("Operation interrupted by button press.")
            os.remove(wavRecordingAddress)
            return 1
    # Process the audio file
    if(os.path.exists(wavRecordingAddress) == False or TestRecord.test_recording(wavRecordingAddress) == -1):
        os.remove(wavRecordingAddress)
        myResponse = "I'm sorry, I didn't catch that. Could you repeat that?"
        have_Conversation2(conversation, transcript, myResponse)
        
    if stop_event.is_set():
            print("Operation interrupted by button press.")
            return 1
    
    transcript = ProcessAudio.ProcessAudio(wavRecordingAddress)
    transcript = re.sub(r'[^a-zA-Z0-9 .,!?-_;()""*:]+', '', transcript)
    print(transcript)
    os.remove(wavRecordingAddress)

    if stop_event.is_set():
            print("Operation interrupted by button press.")
            return 1
    return have_Conversation2(conversation, transcript)


def detect_wake_word2(access_key, wake_word_path):
    import pvporcupine
    import pyaudio
    import struct

    porcupine = None
    pa = None
    audio_stream = None

    try:
        # Initialize Porcupine with the wake word model file
        porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[wake_word_path])

        # Set up audio input stream
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for wake word 'Jarvis'...")

        # Continuously listen and process audio frames
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Check if the wake word was detected
            result = porcupine.process(pcm)
            if result >= 0:
                print("Wake word detected!")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()

    print("Wake word detection completed.")

# The path to the Jarvis wake word model file (you need to replace this with the actual path)
jarvis_model_path = 'Input\Jarvis_en_windows_v3_0_0.ppn'

# Call the wake word detection function

#TestSendCommandToFlipper.SendColorToFlipper("White")
#detect_wake_word2(ACCESS_KEY, jarvis_model_path)
#WhiteChat()
TestSendCommandToFlipper.SendColorToFlipper("Red")
detect_wake_word(ACCESS_KEY, jarvis_model_path)