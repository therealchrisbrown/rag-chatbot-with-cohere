# Frontend libs
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# .env libs
import os
from dotenv import load_dotenv
load_dotenv()

# chatbot class import
from chatbot import Chatbot
from chatbot import Documents

# Define sources
sources = [
    {
        "title": "Text Embeddings", 
        "url": "https://docs.cohere.com/docs/text-embeddings"},
    {
        "title": "Similarity Between Words and Sentences", 
        "url": "https://docs.cohere.com/docs/similarity-between-words-and-sentences"},
    {
        "title": "The Attention Mechanism", 
        "url": "https://docs.cohere.com/docs/the-attention-mechanism"},
    {
        "title": "Transformer Models", 
        "url": "https://docs.cohere.com/docs/transformer-models"}   
]

# Login class with Hugging Face credentials
class Login(Login):
    def __init__(self):
        super().__init__(
            username=os.environ["email_hug"],
            password=os.environ["pw_hug"],
            model="OpenAssistant/oasst-sft-6-llama-30b-xor",
        )

# Create a function that generates the chatbot response by calling the hugchat.generate_response method
def generate_response(user_message):
    response = hugchat.generate_response(
        user_message,
        login=Login(),
        num_tokens=50,
        temperature=0.9,
        top_k=50,
        top_p=0.9,
        num_beams=5,
    )
    return response

# Create a function that displays the chat messages in the streamlit app by calling the st.chat_message method
def display_message(author, text):
    st.chat_message(
        author,
        text,
        color="#F63366" if author == "user" else "#0D6EFD",
        avatar="👩🏻" if author == "user" else "🤖",
        font_size=16,
        border_radius=10,
    )

class App:
    def __init__(self, chatbot: Chatbot):
        """
        Initializes an instance of the App class.

        Parameters:
        chatbot (Chatbot): An instance of the Chatbot class.

        """
        self.chatbot = chatbot
    
    def run(self):
        """
        Runs the chatbot application.

        """
        while True:
            # Get the user message
            message = input("User: ")

            # Typing "quit" ends the conversation
            if message.lower() == "quit":
                print("Ending chat.")
                break
            else:
                print(f"User: {message}")

            # Get the chatbot response
            response = self.chatbot.generate_response(message)

            # Print the chatbot response
            print("Chatbot:")
            flag = False
            for event in response:
                # Text
                if event.event_type == "text-generation":
                    print(event.text, end="")

                # Citations
                if event.event_type == "citation-generation":
                    if not flag:
                        print("\n\nCITATIONS:")
                        flag = True
                    print(event.citations)

            print(f"\n{'-'*100}\n")


if __name__ == "__main__":
    # Assuming Chatbot class has a generate_response method
    documents = Documents(sources)
    chatbot = Chatbot(documents)
    app = App(chatbot)
    app.run()
