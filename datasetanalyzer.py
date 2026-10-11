from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
# filename = input("What is the name of the dataset you would like to analyze? ")
# file = open(f"{filename}")
df = pd.read_csv("student_performance_dataset.csv")
prompt = f"You are a senior data analyst. Analyze and find patterns in {df} and provide important insights. Keep the information short and clean."
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
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
print(response.choices[0].message.content)