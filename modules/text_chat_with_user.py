from modules.answers_modules import answers
from modules.chatgpt_module import text_to_speech



def text_chat_with_user(user_text):
    print('Generating response...');
    try:
        # Generate assistant's response
        assistant_response = answers(user_text)
        # Convert assistant's response to speech
        text_to_speech(assistant_response)

    except Exception as e: 
        print(e);
        return
