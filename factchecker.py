from openai import OpenAI
from dotenv import load_dotenv
import os
#import antigravity


load_dotenv()
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
topic = input("Enter the topic you would like to search: ")
prompt = f"Find out a cool fact about {topic}."
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
print(response.choices[0].message.content)