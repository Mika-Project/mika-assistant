from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import openai

###################################
# CONVERT CHATGPT RESPONSE TO TTS #
###################################

def text_to_speech(text, language='en'):
    print(text)
    tts = gTTS(text=text, lang=language, tld='com.au', slow=False, lang_check=False)
    tts.save('output.mp3')
    audio = AudioSegment.from_file('output.mp3', format='mp3')
    play(audio)
    # Remove the temporary audio file
    os.remove('output.mp3')

def ttsJustText(text, language='en'):
    print(text)
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

conversation_history = "" # Initialize an empty conversation history

def chatgpt(user_message):    
    global conversation_history
    print(conversation_history)
    print("-----------------------------seperator-----------------------------")
    convHistoryLength = len(conversation_history)
    if convHistoryLength >= 1000:
        conversation_history = ""
    print(conversation_history)

    # Append the user message to the conversation history
    conversation_history += f"\nUser: {user_message}"
    
    # Generate a response using OpenAI's API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation_history + "\nAssistant:",
        temperature=0.7,
        max_tokens=500,
        n=1,
        stop=["\n"]
    )

    assistant_message = response.choices[0].text.strip()

    conversation_history += f"\nAssistant: {assistant_message}"

    return assistant_message # Return the response
