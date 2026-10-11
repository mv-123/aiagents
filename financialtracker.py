import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

st.chat_input("What would you like financial help with? ")
prompt = "Think of financial solutions that could help the situation. Think of budgeting plans, saving plans, and help build a step by step solution."

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature=2,
    max_completion_tokens=2048,
    top_p=1,
    stream=False,
    stop=None
)

st.write(response.choices[0].message.content)