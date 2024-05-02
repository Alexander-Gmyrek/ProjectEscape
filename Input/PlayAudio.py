import os
import pygame
import time

def play_mp3(file_path):
    if not (os.path.isfile(file_path)):
        print("File does not exist at the specified location")
    else:
        # Initialize pygame
        pygame.init()

        # Load the MP3 file
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)

        # Play the MP3 file
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        pygame.mixer.quit()