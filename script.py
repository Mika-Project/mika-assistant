from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import openai
import datetime
import webbrowser
import subprocess
from dotenv import load_dotenv
import os
import threading
import time

##############################
# Load environment variables #
##############################

load_dotenv()

###################################
# CONVERT CHATGPT RESPONSE TO TTS #
###################################

def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, tld='com.au', slow=False, lang_check=False)
    tts.save('output.mp3')
    audio = AudioSegment.from_file('output.mp3', format='mp3')
    play(audio)
    # Remove the temporary audio file
    os.remove('output.mp3')

def ttsJustText(text, language='en'):
    tts = gTTS(text=text, lang=language, tld='com.au', slow=False, lang_check=False)
    tts.save('output2.mp3')
    audio = AudioSegment.from_file('output2.mp3', format='mp3')
    play(audio)
    # Remove the temporary audio file
    os.remove('output2.mp3')

#############################
# GET RESPONSE FROM CHATGPT #
#############################

openai.api_key = str(os.getenv('OPENAI_API_KEY'))

def chatgpt(prompt):
    start_sequence = "\nA:"
    restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Q: {prompt}",
        temperature=0.7,
        max_tokens=50,
        n=1,
        stop=None
    )

    # response = response.choices[0].text
    response = response.choices[0].text.strip()
    return response  # Return the generated response

######################
# ANIME PLAY COMMAND #
######################

def run_ani_cli(command):
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    return process.poll()


########################################
# GET RESPONSES AND DO DESIRED ACTIONS #
########################################

def answers(user_input):
    full_text = user_input
    separated_text = user_input.split(" ")
    # print(separated_text[0])
    # print(separated_text[1])

    # Check if user wants to know the time
    if "time" in separated_text and "current" in separated_text:
        # Get the current time
        print("Getting the current time...")
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The time is {current_time}."
    
    # Check if user wants to exit
    elif separated_text[0] == "exit" or separated_text[0] == "quit":
        exit()

    # Check if user wants to know the date
    elif "date" in separated_text and "current" in separated_text:
        # Get the current date
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        return f"The date is {current_date}."
    
    # Check if user wants to know the day
    elif "day" in separated_text and "current" in separated_text:
        # Get the current day
        current_day = datetime.datetime.now().strftime("%A")
        return f"The day is {current_day}."
    
    # Check if user wants to search the web
    elif "go" in separated_text and "to" in separated_text:
        # Find the indices of "go" and "to"
        go_index = separated_text.index("go")
        to_index = separated_text.index("to")

        # Ensure "to" comes after "go"
        if go_index < to_index:
            # Extract the text after "to"
            query = ' '.join(separated_text[to_index + 1:])

            # Check if it is a website
            if "." in query:
                ttsJustText("Going to " + query)
                webbrowser.open("https://" + query)
            else:
                ttsJustText("Searching for " + query)
                webbrowser.open("https://www.google.com/search?q=" + query)
            return "Opening your search query in the browser."
    elif "search" in separated_text and "for" in separated_text:
        # Find the indices of "go" and "to"
        go_index = separated_text.index("search")
        to_index = separated_text.index("for")

        # Ensure "to" comes after "go"
        if go_index < to_index:
            # Extract the text after "to"
            query = ' '.join(separated_text[to_index + 1:])

            ttsJustText("Searching for " + query)
            webbrowser.open("https://www.google.com/search?q=" + query)
            return "Opening your search query in the browser."
    
    # TODO Implement this functionality, but doing it good this time.
    # Check if user wants to watch an anime
    # elif all(word in separated_text for word in ["watch", "anime"]):
    #     watch_index = separated_text.index("watch")
    #     watch_anime = separated_text.index("anime")
        
    #     # Ensure "anime" comes after "watch"
    #     if watch_index < watch_anime:
    #         # Extract the text after "anime"
    #         query = ' '.join(separated_text[watch_anime+1:])

    #         anime_name = "".join(separated_text[2:])
    #         print(f"Watching anime: {query}")
    #         run_ani_cli(f"ani-cli {query}")
    # else:
    #     # Get a response from ChatGPT
    #     response = chatgpt(full_text)
    #     return response

#########################
# LISTER FOR USER INPUT #
#########################

def recognize(recognizer, audio):
    # return sr.Recognizer()
    return recognizer.recognize_whisper(
        audio,      # audio_data
        'small.en', # model can be any of tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en
        False,      # show_dict
        None,       # load_options
        "english",  # language
        False       # translate
    );



def interpret(recognizer, audio):
    print('A voice was heard, recognizing...');

    try:
        user_text = recognize(recognizer, audio);

        if "mika" in user_text.lower():  
            # user_text = user_text.lower().split("mika", 1)[1].strip();
            print("User said:", user_text);

            # Generate assistant's response
            assistant_response = answers(user_text)

            # Convert assistant's response to speech
            text_to_speech(assistant_response)
        else:
            return
    except Exception as e: 
        print(e);

def get_microphone():
    # return default microphone
    return sr.Microphone();
    
def chat_with_user():
    # Initialize the recognizer
    
    r = sr.Recognizer();
    m = get_microphone();
    
    print("Adjusting microphone levels, please be silent");
    with m as source:
        r.adjust_for_ambient_noise(source);

    print("Listening...");
    stop_listening = r.listen_in_background(m, interpret);
    # stop_listening is a function, call it to stop
    
    while True: 
        time.sleep(1.0);
    
# Start the conversation loop
chat_with_user()
