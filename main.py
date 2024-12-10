#Program Modules

import os
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI
import pygame

lang = 'english'                             #language set to English

#Function to get audio from the user and turn it into text
def get_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Hi there, how can I help you?: : ")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)                    #listen for audio input
        translator = r.recognize_google(audio)      #convert the received input to text
        input_statement = str(translator)

        try:
            print("You said: " + translator)
        except sr.UnknownValueError:
            print("Sorry, could not understand audio")
        except sr.RequestError as e:
            print("Could not process the request")

    return input_statement


# Function to send the users request to chatgpt to process using OpenAI API
def process_request():
    user_request = get_audio()

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"{user_request}",
        }],
        model="gpt-3.5-turbo",
    )

    model_response = chat_completion.choices[0].message.content
    print(model_response)
    return model_response


# Function to play Chatgpt's response back to the user
def play_response():
    response_message = process_request()

    # Convert the text to speech and save it as an MP3 file
    speech = gTTS(text=response_message, lang="en")
    speech.save("test.mp3")

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the audio file and play it
    pygame.mixer.music.load("test.mp3")
    pygame.mixer.music.play()

    # Check if the sound is still playing : True or False
    still_playing_checker = pygame.mixer.music.get_busy()

    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():  # Check if the sound is still playing
        pygame.time.Clock().tick(10)

    # If sound checker is set to false, delete the temporary sound file
    if not still_playing_checker:
        try:
            os.remove("test.mp3")  # Remove the file only after the music has finished
            print("File removed successfully.")
        except PermissionError as e:
            print(f"Error deleting the file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return response_message


# Call the function to play the audio
play_response()
