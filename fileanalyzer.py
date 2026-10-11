from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
filename = input("What is the name of the dataset you would like to analyze? ")
file = open(f"{filename}")
prompt = f"Analyze and find patterns in {file.read()}. Do not rewrite the script at all, just provide a basic summary of the file. Keep it minimal."
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