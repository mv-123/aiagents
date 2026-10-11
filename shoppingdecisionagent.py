import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

product = st.text_input("What is the product you would like to buy?")
budget = st.text_input("What is your budget?")
prompt = f"The user wants to buy {product}. Their budget is {budget}, so try to find the item online for that price. If found, attach the link. If the item is too expensive, either try finding something similar or create a plan to save up for the product. If you find a similar item, attach the link."

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

if st.button("Generate"):
    st.write(response.choices[0].message.content)