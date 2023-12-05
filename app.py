import streamlit as st
from chatbot import Chatbot
from chatbot import Documents

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

class App:
    def __init__(self, chatbot: Chatbot):

        self.chatbot = chatbot
    
    def run(self):
        """
        Runs the chatbot application.

        """
        st.title("RAG-Chatbot Application")

        user_input = st.text_input("User", "")

        if st.button("Submit"):
            #Typing "quit" ends the conversation
            if user_input.lower() == "quit":
                st.write("Ending chat.")
            else:
                st.text(f"User: {user_input}")
                        
                #Get response
                response = self.chatbot.generate_response(user_input)
                        
                st.write("Chatbot: ")
                for event in response:
                    # Text
                    if event.event_type == "text-generation":
                        st.write(event.text)

                    # Citations
                    if event.event_type == "citation-generation":
                        st.write("\n\nCITATIONS:")
                        st.write(event.citations)
                st.write(f"\n{'-'*100}\n")

if __name__ == "__main__":
    # Assuming Chatbot class has a generate_response method
    documents = Documents(sources)
    chatbot = Chatbot(documents)
    app = App(chatbot)
    app.run()
