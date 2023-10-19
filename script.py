import speech_recognition as sr
import subprocess
from dotenv import load_dotenv
import os
from modules.answers_modules import answers
from modules.chatgpt_module import text_to_speech
import time

##############################
# Load environment variables #
##############################

load_dotenv()


######################################
# Install requirements automatically #
######################################

def install_dependencies():
    if os.path.exists("installed-dependencies.txt"):
        with open("installed-dependencies.txt", "r") as file:
            content = file.read().strip()
            if content == "true":
                print("Dependencies are already installed.")
                return

    if os.name == 'posix':
        dependencies_script = 'install-requirements.sh'
        try:
            subprocess.run(['sh', dependencies_script], check=True)
            with open("installed-dependencies.txt", "w") as file:
                file.write("true")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")
    elif os.name == 'nt':
        dependencies_script = '.\\install-requirements.bat'
        try:
            subprocess.run([dependencies_script], check=True)
            with open("installed-dependencies.txt", "w") as file:
                file.write("true")
        except subprocess.CalledProcessError as e:
            print(f"Error executing the script: {e}")
    else:
        print("Your OS is not found")

#########################
# LISTER FOR USER INPUT #
#########################

def recognize(recognizer, audio):
    # return sr.Recognizer()
    return recognizer.recognize_whisper(
        audio,      # audio_data
        'small', # model can be any of tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en
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
            print("Mika said:", assistant_response)
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

# DEBUG.
# answer = answers("Hey mika, can you tell me the time")
# text_to_speech(answer)
# while True:
#     time.sleep(1.0)


# Start commands
install_dependencies() # Install dependencies
chat_with_user() # Start the conversation loop