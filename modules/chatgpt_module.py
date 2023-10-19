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