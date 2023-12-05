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
    def __init__(self, documents: Documents, chatbot: Chatbot):
        self.documents = documents
        self.chatbot = chatbot

    def simulate_typing(self, text, delay=0.05):
        """
        Simulate a typing effect by displaying characters with a delay.
        """
        container = st.empty()
        words = text.split()
        typed_text = ""
        for word in words:
            typed_text += word + " "
            container.markdown(typed_text)
            time.sleep(delay)
        container.text("")  # Add a newline after the text


    def run(self):
        st.title("RAG-Chatbot Application")
        user_input = st.text_input("User", "")

        if st.button("Submit"):
            #Typing "quit" ends the conversation
            if user_input.lower() == "quit":
                st.write("Ending chat.")
            else:        
                # Display user input
                st.markdown(f"**User:** {user_input}")

                relevant_docs = self.documents.retrieve(user_input)


                # Display chatbot response with a typing effect
                chatbot_response_placeholder = st.empty()
                for doc in relevant_docs:
                    st.markdown(f"**Title:** {doc['title']}")
                    st.markdown(f"**URL:** [{doc['title']}]({doc['url']})")
                    self.simulate_typing(doc["text"])
                    st.markdown(f"**Answer:** {doc['text']}")
                    st.text(f"")  # Add a newline after the text

                
                # for event in response:
                #     if event.event_type == "text-generation":
                #         self.simulate_typing(event.text)
                #         st.text("")  # Add a newline after the text
                #         #chatbot_response += f"{event.text} "

                #     # Citations
                #     if event.event_type == "citation-generation":
                #         self.simulate_typing(event.citations)
                #         st.text("")  # Add a newline after the citations
                #         #citations += f"{event.citations}\n"
                #         #st.markdown("<hr>", unsafe_allow_html=True)
                #         #st.markdown("**CITATIONS:**", unsafe_allow_html=True)
                #         #st.markdown(event.citations, unsafe_allow_html=True)
                # # Display chatbot response as a coherent paragraph
                # #st.markdown(f"**Chatbot:** {chatbot_response}")

                # # Display citations
                # #if citations:
                # #    st.markdown(f"**Citations:**\n{citations}")
                # chatbot_response_placeholder.text("")  # Clear the placeholder at the end


if __name__ == "__main__":
    # Assuming Chatbot class has a generate_response method
    documents = Documents(sources)
    chatbot = Chatbot(documents)
    app = App(documents, chatbot)
    app.run()
