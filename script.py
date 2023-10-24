import eel
import threading
from dotenv import load_dotenv
from modules.install_dependencies import install_dependencies
from modules.chat_with_user import chat_with_user
from modules.text_chat_with_user import text_chat_with_user

##############################
# Load environment variables #
##############################

load_dotenv()

eel.init("web")

voice_active = False

@eel.expose
def toggleVoice():
    global voice_active
    # Toggle the state of the voice assistant
    voice_active = not voice_active

def startVoice():
    while True:
        if voice_active:
            install_dependencies() # Install dependencies
            chat_with_user() # Start the conversation loop

@eel.expose
def startText(userInput):
    justUserInputString = userInput['FormData']['command']
    userInputResult = text_chat_with_user(justUserInputString)
    print(userInputResult)
    return userInputResult

def start_eel():
    eel.start("index.html", size=(400, 800))

# Create threads for voice and eel
thread1 = threading.Thread(target=startVoice)
thread2 = threading.Thread(target=start_eel)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()