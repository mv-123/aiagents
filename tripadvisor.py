import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

input = st.chat_input("Please enter your destination, budget, your current location, and duration of the trip.")
prompt = f'''Use {input}. You are a trip advisor and planner. 
The user will provide their information in the following format: "destination, budget, current location, duration." 
Use the client's location to find flights from their location to their desired vacation spot. Find a nice hotel in the area and make an itinerary for the desired amount of days including activities and restaurants. Make sure to include flights on the way back as well.'''

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