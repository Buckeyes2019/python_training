import streamlit as st
import requests

st.title("DAD's Old Craig AI")

st.write("Hello Father a.k.a D.O.D. This website was design by your two sons to facilite to answer fishing, kayaking, boating, history etc... questions using Old Craig AI.")

text_input = st.text_area('Enter your question here:')

API_URL = "https://api-inference.huggingface.co/models/gpt2"
#headers = {"Authorization": f"Bearer {API_TOKEN}"}

def ask_GPT_a_question(text_input):
	response = requests.post(API_URL, json=text_input)
	return response.json()

GPT_response = ask_GPT_a_question(text_input)

if st.button("Ask Craig Button") == True:
    st.write(f"{GPT_response[0]['generated_text']}")

#st.image('. /header.png')

