from dotenv import load_dotenv
import eel
from modules.install_dependencies import install_dependencies
from modules.chat_with_user import chat_with_user
from modules.text_chat_with_user import text_chat_with_user

##############################
# Load environment variables #
##############################

load_dotenv()

eel.init("web")

@eel.expose
def startVoice():
    # Start commands
    install_dependencies() # Install dependencies
    chat_with_user() # Start the conversation loop

@eel.expose
def startText(userInput):
    justUserInputString = userInput['FormData']['command']
    userInputResult = text_chat_with_user(justUserInputString)
    print(userInputResult)
    return userInputResult

eel.start("index.html", size=(400, 800))