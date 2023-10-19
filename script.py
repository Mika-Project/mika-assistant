from dotenv import load_dotenv
from modules.install_dependencies import install_dependencies
from modules.chat_with_user import chat_with_user

# Load environment variables 
load_dotenv()



# Start the conversation loop/script
install_dependencies() # Install dependencies
chat_with_user() # Start the conversation loop


# DEBUG.
# answer = answers("Hey mika, can you tell me the current time")
# text_to_speech(answer)