from dotenv import load_dotenv
import eel
from modules.install_dependencies import install_dependencies
from modules.chat_with_user import chat_with_user

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

eel.start("index.html", size=(400, 800))

# DEBUG.
# answer = answers("Hey mika, can you tell me the current time")
# text_to_speech(answer)