import streamlit as st
import time
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
                #Get response
                response = self.chatbot.generate_response(user_input)
                st.markdown(f"**User:** {user_input}")

                chatbot_response = ""
                citations = ""
                
                for event in response:
                    if event.event_type == "text-generation":
                        chatbot_response += f"{event.text} "

                    # Citations
                    if event.event_type == "citation-generation":
                        citations += f"{event.citations}\n"
                        #st.markdown("<hr>", unsafe_allow_html=True)
                        #st.markdown("**CITATIONS:**", unsafe_allow_html=True)
                        #st.markdown(event.citations, unsafe_allow_html=True)
                # Display chatbot response as a coherent paragraph
                st.markdown(f"**Chatbot:** {chatbot_response}")

                # Display citations
                if citations:
                    st.markdown(f"**Citations:**\n{citations}")


if __name__ == "__main__":
    # Assuming Chatbot class has a generate_response method
    documents = Documents(sources)
    chatbot = Chatbot(documents)
    app = App(chatbot)
    app.run()
