import openai
import datetime
import webbrowser
from dotenv import load_dotenv
from modules.chatgpt_module import chatgpt
from modules.anicli_module import run_ani_cli
import os

##############################
# Load environment variables #
##############################

load_dotenv()
openai.api_key = str(os.getenv('OPENAI_API_KEY'))


########################################
# GET RESPONSES AND DO DESIRED ACTIONS #
########################################

def text_chat_with_user(user_input):
    print(user_input)
    full_text = user_input
    separated_text = user_input.split(" ")
    print(separated_text)

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
    elif ("date" in separated_text or "date?" in separated_text) and "current" in separated_text:
        print("Getting the current date...")
        # Get the current date
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        return f"The date is {current_date}."
    
    # Check if user wants to know the day
    elif "day" in separated_text and "current" in separated_text:
        # Get the current day
        current_day = datetime.datetime.now().strftime("%A")
        return f"The day is {current_day}."
    
    # Check if user wants to search the web
    elif "go" in separated_text and "to" in separated_text:
        # Find the indices of "go" and "to"
        go_index = separated_text.index("go")
        to_index = separated_text.index("to")

        # Ensure "to" comes after "go"
        if go_index < to_index:
            # Extract the text after "to"
            query = ' '.join(separated_text[to_index + 1:])

            # Check if it is a website
            if "." in query:
                webbrowser.open("https://" + query)
            else:
                webbrowser.open("https://www.google.com/search?q=" + query)
            return "Opening your search query in the browser."
    elif "search" in separated_text and "for" in separated_text:
        # Find the indices of "go" and "to"
        go_index = separated_text.index("search")
        to_index = separated_text.index("for")

        # Ensure "to" comes after "go"
        if go_index < to_index:
            # Extract the text after "to"
            query = ' '.join(separated_text[to_index + 1:])

            webbrowser.open("https://www.google.com/search?q=" + query)
            return "Opening your search query in the browser."
    # Check if user wants to watch an anime
    elif all(word in separated_text for word in ["watch", "anime"]):
        watch_index = separated_text.index("watch")
        watch_anime = separated_text.index("anime")
        
        # Ensure "anime" comes after "watch"
        if watch_index < watch_anime:
            # Extract the text after "anime"
            query = ' '.join(separated_text[watch_anime+1:])

            anime_name = "".join(separated_text[2:])
            print(f"Searching for anime: {query}")
            run_ani_cli(f"{query}")
    else:
        print("Getting a response from ChatGPT...")
        # Get a response from ChatGPT
        response = chatgpt(full_text)
        return response