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

openai.api_key = 'sk-' + os.getenv('OPENAI_API_KEY')

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
    elif separated_text[0] == "go" and separated_text[1] == "to":
        query = ' '.join(separated_text[2:])
        # check if it is a website
        if "." in query:
            ttsJustText("Going to " + query)
            webbrowser.open("https://" + query)
        else:
            ttsJustText("Searching for " + query)
            webbrowser.open("https://www.google.com/search?q=" + query)
        return "Opening your search query in the browser."
    
    # Check if user wants to watch an anime
    elif all(word in separated_text for word in ["watch", "anime"]):
        anime_name = "".join(separated_text[2:])
        print(f"Watching anime: {anime_name}")
        run_ani_cli(f"ani-cli {anime_name}")

    else:
        # Get a response from ChatGPT
        response = chatgpt(full_text)
        return response

#########################
# LISTER FOR USER INPUT #
#########################

def chat_with_user():
    # Initialize the recognizer
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("[STATUS] - Adjusting for ambient noise level.")
            r.adjust_for_ambient_noise(source)

            print("[STATUS] - Listening...")
            audio = r.listen(source)  # Increase the timeout as needed

            try:
                speech_text = r.recognize_google(audio)
                print("Recognized:", speech_text)

                if "mika" in speech_text.lower():
                    print("Assistant activated.")

                    try:
                        print("Listening to user...")
                        user_audio = r.listen(source, timeout=5)
                        user_text = r.recognize_google(user_audio)
                        print("User said:", user_text)

                        # Generate assistant's response
                        assistant_response = answers(user_text)

                        # Convert assistant's response to speech
                        text_to_speech(assistant_response)

                    except sr.WaitTimeoutError:
                        print("No speech detected.")

                    except sr.UnknownValueError:
                        print("[ERROR] - Unable to recognize user speech.")

            except sr.WaitTimeoutError:
                print("No speech detected within timeout.")

            except sr.UnknownValueError:
                print("[ERROR] - Unable to recognize speech.")

# Start the conversation loop
chat_with_user()
