import time
import speech_recognition as sr
from modules.answers_modules import answers
from modules.chatgpt_module import text_to_speech

#########################
# LISTER FOR USER INPUT #
#########################

def recognize(recognizer, audio):
    # return sr.Recognizer()
    return recognizer.recognize_whisper(
        audio,      # audio_data
        'small',    # model can be any of tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en
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