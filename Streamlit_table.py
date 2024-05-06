import streamlit as st
import pandas as pd

class DataFrameComponent:
    def __init__(self):
        self.df = None

    def render(self):
        if self.df is None:
            return ""
        else:
            return f"<table>{self.df.to_html()}</table>"

    def update(self, df):
        self.df = df

    def add_to_chat_history(self, chat_history):
        chat_history.append({"role": "dataframe", "content": self.render()})

# Example usage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

df_component = DataFrameComponent()

user_input = st.chat_input("Enter your message")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Add your logic to generate the assistant's response
    assistant_response = "This is a sample response from the assistant."
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Update the DataFrame and add it to the chat history
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_component.update(df)
    df_component.add_to_chat_history(st.session_state.chat_history)

def display_chat_history():
    for message in st.session_state.chat_history:
        if message["role"] == "dataframe":
            st.components.v1.html(message["content"], height=500, width=800)
        else:
            with st.chat_message(name=message["role"]):
                st.write(message["content"])

display_chat_history()
