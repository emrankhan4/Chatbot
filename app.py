# src/frontend/app.py

import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/ask"

st.title("Knowledge-Based Chatbot")

st.write("Ask any question about NIKLES")

# Initialize the chat history
if "history" not in st.session_state:
    st.session_state.history = []

def send_query(question):
    response = requests.post(API_URL, json={"question": question})
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        return "Error: Could not get the answer."

# Function to handle new user input
def handle_input():
    question = st.session_state["new_question"]
    if question:
        answer = send_query(question)
        st.session_state.history.append(("👤", question))
        st.session_state.history.append(("🤖", answer))
        # Clear the input field
        st.session_state["new_question"] = ""

# Custom CSS for chat messages
st.markdown("""
    <style>
        .user-message {
            background-color: #1E3A8A;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            width: fit-content;
            max-width: 70%;
            word-wrap: break-word;
        }
        .bot-message {
            background-color: #F8F9FA;
            color: black;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            width: fit-content;
            max-width: 70%;
            word-wrap: break-word;
        }
    </style>
""", unsafe_allow_html=True)

# Display chat history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"<div class='user-message' style='background-color: powderblue'  ><b>{sender} </b> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'><b>{sender} </b> {message}</div>", unsafe_allow_html=True)

# User input
st.text_input("You:", key="new_question", on_change=handle_input)
